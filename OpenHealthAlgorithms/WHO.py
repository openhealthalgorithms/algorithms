#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import math
import numpy as np
import os

from OpenHealthAlgorithms.__helpers import format_params

__author__ = "indrajit"
__license__ = "Apache License"
__version__ = "0.1.1"
__maintainer__ = "indrajit"
__email__ = "eendroroy@gmail.com"


class WHO(object):
    """
    Calculates Diabetes risk score

    Example
    -------
        >>> from OpenHealthAlgorithms.WHO import WHO
        >>> params = {
        ...    'gender': "M", 'age': 30 ,'systolic_blood_pressure_1':  130,
        ...    'systolic_blood_pressure_2': 145, 'cholesterol': 7.0,
        ...    'is_smoker': "Y", 'has_diabetes': "Y"
        ... }
        >>> result = WHO().calculate(params)
        >>> print(result)

    """

    @staticmethod
    def __convert_age(age):
        if age <= 18:
            return 0
        elif age <= 50:
            return 40
        elif age <= 60:
            return 50
        elif age <= 70:
            return 60
        elif age <= 80:
            return 70
        else:
            return None

    @staticmethod
    def __convert_sbp(systolic_blood_pressure):
        if systolic_blood_pressure <= 140:
            return 3
        elif 140 < systolic_blood_pressure <= 160:
            return 2
        elif 160 < systolic_blood_pressure <= 180:
            return 1
        elif systolic_blood_pressure > 180:
            return 0

    @staticmethod
    def __convert_cholesterol(cholesterol):
        _cholesterol = float(cholesterol)
        temp_cholesterol_index = math.ceil(_cholesterol) - 4

        if temp_cholesterol_index < 1:
            return 0
        elif temp_cholesterol_index <= 4:
            return temp_cholesterol_index

    @staticmethod
    def __convert_risk(cvd_risk):
        if cvd_risk == 10:
            return "<10%"
        elif cvd_risk == 20:
            return "10-20%"
        elif cvd_risk == 30:
            return "20-30%"
        elif cvd_risk == 40:
            return "30-40%"
        elif cvd_risk == 50:
            return "> 40%"
        else:
            return "UNIDENTIFIED"

    @staticmethod
    def calculate(params):
        """

        Parameters
        ----------
        params: dict
            dictionary includes 'gender', 'age', 'systolic_blood_pressure_1',
            'systolic_blood_pressure_2', 'cholesterol', 'is_smoker',
            'has_diabetes'

        Example
        -------
            >>> params = {
            ...    'gender':                     "M",
            ...    'age':                        30,
            ...    'systolic_blood_pressure_1':  130,
            ...    'systolic_blood_pressure_2':  145,
            ...    'cholesterol':                5,
            ...    'is_smoker':                  "Y",
            ...    'has_diabetes':               "Y",
            ... }
            >>> WHO().calculate(params)

        Returns
        -------
        dict
            Diabetes risk score
        """

        # ToDo: add parameter validations

        params = format_params(params)

        cholesterol = WHO.__convert_cholesterol(params['cholesterol']) \
            if 'cholesterol' in params.keys() else 'uc '
        diabetes = params['has_diabetes']
        gender = params['gender']
        smoker = params['is_smoker']
        age = str(WHO.__convert_age(params['age']))
        sbp1 = params['systolic_blood_pressure_1']
        sbp2 = params['systolic_blood_pressure_2']
        sbp_index = WHO.__convert_sbp((sbp1 + sbp2) / 2)

        filename = ("%s_%s_%s_%s_%s.txt" % (
            cholesterol if cholesterol == 'uc' else 'c',
            'd' if str(diabetes).upper() == 'Y' else 'ud',
            str(gender).lower(),
            's' if str(smoker).upper() == 'Y' else 'ns',
            str(age)
        ))

        file_path = ("%s/who_files/%s" % (
            os.path.dirname(os.path.realpath(__file__)),
            filename
        ))

        data = np.loadtxt(file_path, dtype=int, delimiter=',')

        risk = data[sbp_index] if cholesterol == 'uc' else data[sbp_index, cholesterol]

        return {'risk': risk, 'risk_range': WHO.__convert_risk(risk)}
