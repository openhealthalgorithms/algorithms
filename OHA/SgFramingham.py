#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from OHA.__helpers import format_params, find_age_index
from OHA.__unit import convert_cholesterol_unit
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder
from OHA.helpers.formatters.ParamFormatter import ParamFormatter

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class SgFramingham(object):
    """
        Modified FRE based on the SG MoH CVD Guidelines
    """
    __default_cholesterol_unit = 'mmol/L'

    # co-efficients used in the calculation. See relevant paper
    @staticmethod
    def __get_co_efficient(key, gender):
        return Framingham.__co_efficients[key][gender]

    @staticmethod
    def age_modifier_fre_points(age, gender):

        age_brackets = ['20-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79']
        age_points = {
            "m" : [-9, -4, 0, 3, 6, 8, 10, 11, 12, 13],
            "f" : [-7, -3, 0, 3, 6, 8, 10, 12, 14, 16]
        } 

        index = 0
        value = None
        bracket = find_age_index(age, age_brackets)
        index = age_brackets.index(bracket)
        
        gender = gender.lower()
        if index >= 0:
            value = age_points[gender][index]
        
        return value   

    @staticmethod
    def calculate_smoking_points(age, gender):

        age_brackets = ['20-39', '40-49', '50-59', '60-69', '70-79']
        smoking_points = {
            "m" : [8, 5, 3, 1, 0],
            "f" : [9, 7, 4, 2, 1]
        }

        # Based on the age, look up the index
        # For the given index in the points array return the value
        
        index = 0
        value = None
        gender = gender.lower()

        bracket = find_age_index(age, age_brackets)
        index = age_brackets.index(bracket)
        # should check we have a valid index
        if index >= 0:
            value = smoking_points[gender.lower()][index]
            
        return value    

    @staticmethod
    def calculate_cholesterol_points(age, gender, total_cholesterol, hdl_cholesterol):
    
        age_brackets = ['20-39', '40-49', '50-59', '60-69', '70-79']
        
        if gender.lower() == 'm':
            chol_points = np.array([[0, 0, 0, 0, 0], [4, 3, 2, 1, 0], [7, 5, 3, 1, 0], [9, 6, 4, 2, 1], [11, 8, 5, 3, 1]])
        elif gender.lower() == 'f':
            chol_points = np.array([[0, 0, 0, 0, 0], [4, 3, 2, 1, 1], [8, 6, 4, 2, 1], [11, 8, 5, 3, 2], [13, 10, 7, 4, 2]])
        
        row_names = ['<4.1', '4.1-5.1', '5.2-6.1', '6.2-7.2','>=7.3']
        
        tchol_points_df = pd.DataFrame(chol_points, index=row_names, columns=age_brackets)
            
        # first check the cholesterol range and get the row_index
        
        if total_cholesterol < 4.1:
            chol_range = '<4.1'
        elif total_cholesterol <= 5.1:
            chol_range = '4.1-5.1'
        elif total_cholesterol <= 6.1:
            chol_range = '5.2-6.1'
        elif total_cholesterol <= 7.2:
            chol_range = '6.2-7.2'
        elif total_cholesterol >= 7.3:
            chol_range = '>=7.3'
        else:
            chol_range = '>=7.3'

        # then return the column index based on age range
        age_index = find_age_index(age, age_brackets)

        # look up the value from the df
        # looking up with keys
        cholesterol_points = tchol_points_df[age_index][chol_range]

        if hdl_cholesterol < 1.0:
            hdl_points = +2
        elif hdl_cholesterol <= 1.2:
            hdl_points = 1
        elif hdl_cholesterol <= 1.5:
            hdl_points = 0
        elif hdl_cholesterol >= 1.6:
            hdl_points = -1
                    
        cholesterol_points = cholesterol_points + hdl_points
        
        return cholesterol_points

    @staticmethod
    def calculate_bp_points(gender, sbp, sbp_rx):

        row_names = ['<120', '120-129', '130-139', '140-159', '>=160']
        col_names = ['treated', 'untreated']

        if gender == 'm':
            sbp_points = np.array([[0, 0], [0, 1], [1, 2], [1, 2], [2, 3]])
        elif gender == 'f':
            sbp_points = np.array([[0, 0], [1, 3], [2, 4], [3, 5], [4, 6]])
        else:
            sbp_points = np.array([[0, 0], [1, 3], [2, 4], [3, 5], [4, 6]])

        bp_df = pd.DataFrame(sbp_points, index=row_names, columns=col_names)

        if sbp < 120:
            sbp_index = '<120'
        elif sbp < 130:
            sbp_index = '120-129'
        elif sbp < 140:
            sbp_index = '130-139'
        elif sbp < 160:
            sbp_index = '140-159'
        elif sbp >= 160:
            sbp_index = '>=160'
        else:
            sbp_index = '>=160'

        if sbp_rx:
            col_index = 'treated'
        else:
            col_index = 'untreated'

        bp_points = bp_df[col_index][sbp_index]

        return bp_points

    @staticmethod
    def calculate_fre_score(params):
        # Unpack the parameters
        gender = params.get('gender')
        age = params.get('age')
        ethnicity = params.get('ethnicity')
        total_cholesterol = convert_cholesterol_unit(
            params.get('total_cholesterol'),
            params.get('cholesterol_unit') or SgFramingham.__default_cholesterol_unit,
            SgFramingham.__default_cholesterol_unit,
        )
        hdl_cholesterol = convert_cholesterol_unit(
            params.get('hdl_cholesterol'),
            params.get('cholesterol_unit') or SgFramingham.__default_cholesterol_unit,
            SgFramingham.__default_cholesterol_unit,
        )
        on_bp_medication = params.get('bp_medication')
        systolic = params.get('systolic')
        is_smoker = params.get('is_smoker')
        # has_diabetes = params.get('has_diabetes')

        age_points = SgFramingham().age_modifier_fre_points(age, gender)

        if is_smoker:
            smoking_points = SgFramingham().calculate_smoking_points(age, gender)
        else:
            smoking_points = 0

        cholesterol_points = SgFramingham().calculate_cholesterol_points(
            age, gender, total_cholesterol, hdl_cholesterol,
        )

        sbp_points = SgFramingham().calculate_bp_points(gender, systolic, on_bp_medication)

        fre_points = int(age_points) + int(smoking_points) + int(cholesterol_points) + int(sbp_points)

        # convert the points to a score based
        col_names = ['chinese', 'malay', 'indian']
        if gender == 'm':
            filename = 'OHA/sg_risk/sg_10year_risk_male.csv'
        else:
            filename = 'OHA/sg_risk/sg_10year_risk_female.csv'

        fre_pd = pd.read_csv(filename, header=0, index_col=0)
        fre_risk = fre_pd[col_names]
        # look up the risk score based on the dataframe
        fre_risk_score = fre_risk[ethnicity][fre_points]
        return fre_risk_score

    @staticmethod
    def cvd_risk_level(cvd_risk):

        if cvd_risk < 10:
            return 'Low'
        elif cvd_risk < 15:
            return 'Medium'
        elif cvd_risk >= 15:
            return 'High'

    @staticmethod
    def calculate(params):
        """

        Parameters
        ----------
        params: dict
            Dictionary includes 'gender', 'ethnicity', age', 'total_cholesterol',
            'hdl_cholesterol', 'systolic', 'on_bp_medication',
            'is_smoker', 'has_diabetes'.

        Example
        -------
           >>> params = {
           ...    'gender':                 'M',
           ...    'age':                    40,
           ...    'ethnicity':              'malay',
           ...    'total_cholesterol':      180,
           ...    'cholesterol_unit':       'mg/dl',
           ...    'hdl_cholesterol':        45,
           ...    'systolic':               125,
           ...    'on_bp_medication':       False,
           ...    'is_smoker':              False,
           ...    'has_diabetes':           False,
           ... }
           >>> SgFramingham().calculate(params)

        Returns
        -------
        dict
           Framingham risk score and heart age and risk_range
        """
        params = ParamFormatter(params).formatted
        print(params)

        cvd_risk = int(SgFramingham().calculate_fre_score(params))
        heart_age = None
        # heart_age = SgFramingham.__calculate_heart_age(cvd_risk, params['gender'])
        risk_range = SgFramingham().cvd_risk_level(cvd_risk)

        return {
            'raw_risk': float('%.4f' % (round(cvd_risk, 4))),
            'risk': cvd_risk,
            'heart_age': heart_age,
            'risk_range': risk_range,
        }

    @staticmethod
    def get_sample_params():
        return FraminghamParamsBuilder() \
            .gender('F') \
            .age(40) \
            .ethnicity('malay') \
            .t_chol(170, 'mg/dl') \
            .hdl_chol(45, 'mg/dl') \
            .sbp(125) \
            .build()
