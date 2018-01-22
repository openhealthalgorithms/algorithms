#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from OHA.Defaults import Defaults
from OHA.__unit import convert_height_unit, convert_weight_unit
from OHA.__utilities import calculate_bmi, calculate_waist_hip_ratio
from OHA.helpers.formatters.ParamFormatter import ParamFormatter
from OHA.helpers.measurements.BMI import BMI
from OHA.helpers.measurements.WaistHipRatio import WaistHipRatio
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class Diabetes(object):
    """
    Calculates Diabetes risk score

    Example
    -------
        >>> from OHA.Diabetes import Diabetes
        >>> params = {
        ...    'gender': 'M', 'age': 31, 'systolic': 139, 'diastolic': 90,
        ...    'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0,
        ... }
        >>> result = Diabetes().calculate(params)
        >>> print(result)

    """

    @staticmethod
    def __adjust_risk_by_gender_and_whi(risk_score, gender, waist_hip_ratio):
        if gender == 'M' and waist_hip_ratio < 0.9:
            risk_score += 2
        elif gender == 'M' and waist_hip_ratio >= 0.9:
            risk_score += 7
        elif waist_hip_ratio >= 0.8:
            risk_score += 5
        return risk_score

    @staticmethod
    def __adjust_risk_by_age(risk_score, age):
        if 30 < age < 41:
            risk_score += 3
        elif age > 40:
            risk_score += 4
        return risk_score

    @staticmethod
    def __adjust_risk_by_bmi(risk_score, body_mass_index):
        if body_mass_index >= 25:
            risk_score += 2
        return risk_score

    @staticmethod
    def __adjust_risk_by_bp(
            risk_score,
            systolic_blood_pressure,
            diastolic_blood_pressure,
    ):
        # ToDo:
        # need to clarify this is it AND or OR
        # should be the average of two readings
        if systolic_blood_pressure >= 140 or diastolic_blood_pressure >= 90:
            risk_score += 2
        return risk_score

    @staticmethod
    def calculate(params):
        """

        Parameters
        ----------
        params: dict
            dictionary includes 'gender', 'age',
            'systolic' and  'diastolic' blood pressures,
            'weight', 'height', 'waist', and 'hip'.

        Example
        -------
            >>> params = {
            ...    'gender':      'M',
            ...    'age':         30,
            ...    'systolic':    145,
            ...    'diastolic':   80,
            ...    'weight':      70.0,
            ...    'weight_unit': 'kg',
            ...    'height':      1.5,
            ...    'height_unit': 'm',
            ...    'waist':       99.0,
            ...    'waist_unit':  'cm',
            ...    'hip':         104.0,
            ...    'hip_unit':    'cm',
            ... }
            >>> Diabetes().calculate(params)

        Returns
        -------
        dict
            Diabetes risk score
        """

        # ToDo: add parameter validations

        params = ParamFormatter(params).formatted

        # print('height param = %s ' % params.get('height'))

        gender = params.get('gender')
        age = params.get('age')
        systolic_blood_pressure = params.get('systolic')
        diastolic_blood_pressure = params.get('diastolic')
        waist_hip_ratio = WaistHipRatio(
            convert_height_unit(
                params.get('waist'),
                params.get('waist_unit') or Defaults.waist_unit,
                Defaults.waist_unit,
            ),
            convert_height_unit(
                params.get('hip'),
                params.get('hip_unit') or Defaults.hip_unit,
                Defaults.hip_unit,
            ),
        ).whr
        body_mass_index = BMI(
            convert_weight_unit(
                params.get('weight'),
                params.get('weight_unit') or Defaults.weight_unit,
                Defaults.weight_unit,
            ),
            convert_height_unit(
                params.get('height'),
                params.get('height_unit') or Defaults.height_unit,
                Defaults.height_unit,
            ),
        ).bmi

        risk_score = 0
        risk_score = Diabetes.__adjust_risk_by_gender_and_whi(
            risk_score,
            gender,
            waist_hip_ratio,
        )
        risk_score = Diabetes.__adjust_risk_by_age(risk_score, age)
        risk_score = Diabetes.__adjust_risk_by_bmi(risk_score, body_mass_index)
        risk_score = Diabetes.__adjust_risk_by_bp(
            risk_score,
            systolic_blood_pressure,
            diastolic_blood_pressure,
        )

        if risk_score >= 9:
            result_code = 'DM-1'
        else:
            result_code = 'DM-0'

        return {
            'risk': risk_score,
            'waist_hip_ratio': float('%.2f' % (round(waist_hip_ratio, 2))),
            'body_mass_index': float('%.2f' % (round(body_mass_index, 2))),
            'code': result_code,
        }

    @staticmethod
    def get_sample_params():
        return DiabetesParamsBuilder() \
            .gender('M') \
            .age(40) \
            .sbp(150) \
            .dbp(92) \
            .weight(92, 'kg') \
            .height(1.5, 'm') \
            .waist(50, 'cm') \
            .hip(90, 'cm') \
            .build()
