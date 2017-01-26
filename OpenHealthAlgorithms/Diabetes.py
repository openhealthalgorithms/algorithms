#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# ToDo: insert file headers
__author__ = ""
__copyright__ = ""

__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = ""


class Diabetes(object):
    """
    Calculates Diabetes risk score

    Example
    -------
        >>> from OpenHealthAlgorithms.Diabetes import Diabetes
        >>> params = {
        ...    'gender': 'M', 'age': 31, 'systolic': 139, 'diastolic': 90,
        ...    'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0
        ... }
        >>> result = Diabetes().calculate(params)
        >>> print result

    """
    @staticmethod
    def __calculate_waist_hip_ratio(waist, hip):
        waist_hip_ratio = waist / hip
        return waist_hip_ratio

    @staticmethod
    def __calculate_body_mass_index(weight, height):
        body_mass_index = weight / (height * height)
        return body_mass_index

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
            ...    'gender':    "M",
            ...    'age':       30,
            ...    'systolic':  145,
            ...    'diastolic': 80,
            ...    'weight':    70.0,
            ...    'height':    1.5,
            ...    'waist':     99.0,
            ...    'hip':       104.0,
            ... }
            >>> Diabetes().calculate(params)

        Returns
        -------
        dict
            Diabetes risk score
        """

        # ToDo: add parameter validations

        params = {
            key: float(value) if type(value) is int else value
            for key, value in params.iteritems()
        }

        gender = params.get('gender')
        age = params.get('age')
        systolic_blood_pressure = params.get('systolic')
        diastolic_blood_pressure = params.get('diastolic')
        waist_hip_ratio = Diabetes.__calculate_waist_hip_ratio(
            params.get('waist'),
            params.get('hip')
        )
        body_mass_index = Diabetes.__calculate_body_mass_index(
            params.get('weight'),
            params.get('height')
        )

        risk_score = 0

        if gender == "M" and waist_hip_ratio < 0.9:
            risk_score += 2
        elif gender == "M" and waist_hip_ratio >= 0.9:
            risk_score += 7
        elif waist_hip_ratio >= 0.8:
            risk_score += 5

        if 30 < age < 41:
            risk_score += 3
        elif age > 40:
            risk_score += 4

        if body_mass_index >= 25:
            risk_score += 2

        # ToDo:
        # need to clarify this is it AND or OR
        # should be the average of two readings
        if systolic_blood_pressure >= 140 or diastolic_blood_pressure >= 90:
            risk_score += 2

        return {
            'risk_score':      risk_score,
            'waist_hip_ratio': round(waist_hip_ratio, 2),
            'body_mass_index': round(body_mass_index, 2),
        }
