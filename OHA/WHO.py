#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import math
import os

import numpy as np

from OHA.__helpers import format_params
from OHA.__unit import convert_cholesterol_unit
from OHA.param_builders.who_param_builder import WhoParamsBuilder

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class WHO(object):
    """
    Calculates Diabetes risk score

    Example
    -------
        >>> from OHA.WHO import WHO
        >>> params = {
        ...    'gender': "M", 'age': 30 ,'systolic_blood_pressure_1':  130,
        ...    'systolic_blood_pressure_2': 145, 'cholesterol': 7.0,
        ...    'is_smoker': True, 'has_diabetes': True
        ... }
        >>> result = WHO().calculate(params)
        >>> print(result)

    """

    __default_cholesterol_unit = 'mmol/l'

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
        else:
            return 4

    @staticmethod
    def __convert_risk(cvd_risk):
        if cvd_risk == 10:
            return '<10%'
        elif cvd_risk == 20:
            return '10-20%'
        elif cvd_risk == 30:
            return '20-30%'
        elif cvd_risk == 40:
            return '30-40%'
        elif cvd_risk == 50:
            return '> 40%'
        else:
            return '> 40%'

    @staticmethod
    def calculate(params):
        """

        Parameters
        ----------
        params: dict
            dictionary includes 'gender', 'age', 'systolic_blood_pressure_1',
            'systolic_blood_pressure_2', 'cholesterol', 'is_smoker',
            'has_diabetes', 'region'

        Example
        -------
            >>> params = {
            ...    'gender':                     "M",
            ...    'age':                        30,
            ...    'systolic_blood_pressure_1':  130,
            ...    'systolic_blood_pressure_2':  145,
            ...    'cholesterol':                5,
            ...    'cholesterol_unit':           'mmol/l',
            ...    'is_smoker':                  True,
            ...    'has_diabetes':               True,
            ...    'region':                     'SEARD',
            ... }
            >>> WHO().calculate(params)

        Returns
        -------
        dict
            Diabetes risk score
        """

        # ToDo: add parameter validations

        params = format_params(params)

        cholesterol = WHO.__convert_cholesterol(
            convert_cholesterol_unit(
                params.get('cholesterol'),
                params.get('cholesterol_unit') or WHO.__default_cholesterol_unit,
                WHO.__default_cholesterol_unit
            )
        ) if 'cholesterol' in params.keys() else 'uc'
        diabetes = params.get('has_diabetes')
        gender = params.get('gender')
        smoker = params.get('is_smoker')
        age = str(WHO.__convert_age(params.get('age')))
        sbp1 = params.get('systolic_blood_pressure_1')
        sbp2 = params.get('systolic_blood_pressure_2')
        sbp_index = WHO.__convert_sbp((sbp1 + sbp2) / 2)
        region = params.get('region') if 'region' in params.keys() else 'SEARD'

        filename = ('%s_%s_%s_%s_%s.txt' % (
            cholesterol if cholesterol == 'uc' else 'c',
            'd' if diabetes else 'ud',
            str(gender).lower(),
            's' if smoker else 'ns',
            str(age)
        ))

        file_path = ('%s/color_charts/%s/%s' % (
            os.path.dirname(os.path.realpath(__file__)),
            region,
            filename
        ))

        try:
            data = np.loadtxt(file_path, dtype=int, delimiter=',')
            risk = data[sbp_index] if cholesterol == 'uc' \
                else data[sbp_index, cholesterol]
            return {
                'risk': int(risk),
                'risk_range': WHO.__convert_risk(int(risk))
            }
        except IOError:
            return {
                'risk': None,
                'risk_range': None,
                'exception': 'color chart not found.'
            }

    @staticmethod
    def get_sample_params():
        return WhoParamsBuilder() \
            .gender("M")\
            .age(70)\
            .sbp1(130)\
            .sbp2(145)\
            .chol(270, 'mg/dl')\
            .smoker()\
            .diabetic()\
            .build()
