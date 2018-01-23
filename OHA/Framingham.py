#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import numpy as np

from OHA.__unit import convert_cholesterol_unit
from OHA.helpers.formatters.ParamFormatter import ParamFormatter
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class Framingham(object):
    """

    """

    __co_efficients = {
        'so10': {'F': 0.95012, 'M': 0.8893},
        'logAge': {'F': 2.32888, 'M': 3.06117},
        'logTChol': {'F': 1.20904, 'M': 1.12370},
        'logHDLChol': {'F': 0.70833, 'M': 0.93263},
        'logSBPNonRx': {'F': 2.76157, 'M': 1.93303},
        'logSBPRx': {'F': 2.82263, 'M': 1.99881},
        'logSmoking': {'F': 0.52873, 'M': 0.65451},
        'logDM': {'F': 0.69154, 'M': 0.57367},
        'calc_mean': {'F': 26.1931, 'M': 23.9802},
    }

    __default_cholesterol_unit = 'mg/dl'

    # co-efficients used in the calculation. See relevant paper
    @staticmethod
    def __get_co_efficient(key, gender):
        return Framingham.__co_efficients[key][gender]

    @staticmethod
    def calculate_fre_score(params):
        gender = params.get('gender')
        age = params.get('age')
        total_cholesterol = convert_cholesterol_unit(
            params.get('total_cholesterol'),
            params.get('total_cholesterol_unit') or Framingham.__default_cholesterol_unit,
            Framingham.__default_cholesterol_unit,
        )
        hdl_cholesterol = convert_cholesterol_unit(
            params.get('hdl_cholesterol'),
            params.get('hdl_cholesterol_unit') or Framingham.__default_cholesterol_unit,
            Framingham.__default_cholesterol_unit,
        )
        on_bp_medication = params.get('on_bp_medication')
        systolic = params.get('systolic')
        is_smoker = params.get('is_smoker')
        has_diabetes = params.get('has_diabetes')

        risk_chol = (
                Framingham.__get_co_efficient('logAge', gender)
                * np.log(age)
                + Framingham.__get_co_efficient('logTChol', gender)
                * np.log(total_cholesterol)
                - Framingham.__get_co_efficient('logHDLChol', gender)
                * np.log(hdl_cholesterol)
        )

        # If on medication for BP
        if on_bp_medication:
            risk_systolic = (
                    Framingham.__get_co_efficient('logSBPRx', gender)
                    * np.log(systolic)
            )
        else:
            risk_systolic = (
                    Framingham.__get_co_efficient('logSBPNonRx', gender)
                    * np.log(systolic)
            )

        risk_smoking = (
                Framingham.__get_co_efficient('logSmoking', gender)
                * is_smoker
        )
        risk_diabetes = (
                Framingham.__get_co_efficient('logDM', gender)
                * has_diabetes
        )
        total_risk = risk_chol + risk_systolic + risk_smoking + risk_diabetes

        framingham_risk_score = 1 - np.power(
            Framingham.__get_co_efficient('so10', gender),
            np.exp(total_risk - Framingham.__get_co_efficient('calc_mean', gender)),
        )

        return framingham_risk_score

    @staticmethod
    def __calculate_heart_age(cvd_risk, gender, age):

        '''
            return the ideal heart age which is the heart age based on age and gender with no risk factors
            also approximate the heart age given the cvd_risk
        '''

        standard_params = {
            'age' : age,
            'gender': gender,
            'total_cholesterol': 120,
            'total_cholesterol_unit' : 'mg/dl',
            'hdl_cholesterol': 60,
            'hdl_cholesterol_unit' : 'mg/dl',
            'systolic': 120,
            'on_bp_medication': False,
            'is_smoker': False,
            'has_diabetes': False,
        }

        standard_cvd_risk = round(Framingham.calculate_fre_score(standard_params) * 100, 2)
        cvd_risk = round(cvd_risk * 100, 2)
 
        # run a binary search to estimate heart age
        # to calculate the heart age, search for the age that would give ideal_cvd_risk == cvd_risk
        # if the cvd_risk is > than the ideal .. then we are looking for an age greater
        # otherwise, looking for an age lower
        
        heart_age = age
        search_age = 30
        if cvd_risk > standard_cvd_risk:
            search_age = age
        
        while search_age <= 100:
            standard_params['age'] = search_age
            calc_risk = round(Framingham.calculate_fre_score(standard_params) * 100, 2)
            if calc_risk >= cvd_risk:
                heart_age = search_age
                break
            else:
                search_age = search_age+1
        else:
            heart_age = search_age
        
        return float(standard_cvd_risk), heart_age
        
    @staticmethod
    def cvd_risk_level(cvd_risk):

        if cvd_risk < 10:
            return '<10'
        elif cvd_risk < 20:
            return '10-20'
        elif cvd_risk < 30:
            return '20-30'
        elif cvd_risk < 40:
            return '30-40'
        else:
            return '>40'

    @staticmethod
    def calculate(params):
        """

        Parameters
        ----------
        params: dict
            Dictionary includes 'gender', age', 'total_cholesterol',
            'hdl_cholesterol', 'systolic', 'on_bp_medication',
            'is_smoker', 'has_diabetes'.

        Example
        -------
           >>> params = {
           ...    'gender':                 'M',
           ...    'age':                    40,
           ...    'total_cholesterol':      180,
           ...    'total_cholesterol_unit': 'mg/dl',
           ...    'hdl_cholesterol':        45,
           ...    'hdl_cholesterol_unit':   'mg/dl',
           ...    'systolic':               125,
           ...    'on_bp_medication':       False,
           ...    'is_smoker':              False,
           ...    'has_diabetes':           False,
           ... }
           >>> Framingham().calculate(params)

        Returns
        -------
        dict
           Framingham risk score and heart age and risk_range
        """

        params = ParamFormatter(params).formatted
        cvd_risk = Framingham.calculate_fre_score(params)
        heart_age_calc = Framingham.__calculate_heart_age(cvd_risk, params['gender'], params['age'])
        risk_range = Framingham.cvd_risk_level(cvd_risk * 100)

        return {
            'raw_risk': float('%.4f' % (round(cvd_risk, 4))),
            'risk': round(cvd_risk * 100, 2),
            'normal_risk' : heart_age_calc[0],
            'heart_age': heart_age_calc[1],
            'risk_range': risk_range,
        }

    @staticmethod
    def get_sample_params():
        return FraminghamParamsBuilder() \
            .gender('F') \
            .age(40) \
            .t_chol(170, 'mg/dl') \
            .hdl_chol(45, 'mg/dl') \
            .sbp(125) \
            .build()
