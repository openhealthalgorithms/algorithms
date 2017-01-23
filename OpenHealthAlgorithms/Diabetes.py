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
        >>> risk_score = Diabetes().risk_score(params)
        >>> print risk_score
        7

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
    def risk_score(params):
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

        Returns
        -------
        int
            Diabetes risk score
        """

        # ToDo: add parameter validations

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

        calculated_risk_score = 0

        if gender == "M":
            calculated_risk_score += 2
            if waist_hip_ratio >= 0.9:
                calculated_risk_score += 5
        else:
            if waist_hip_ratio >= 0.8:
                calculated_risk_score += 5

        if 30 < age < 41:
            calculated_risk_score += 3
        elif age > 40:
            calculated_risk_score += 4

        if body_mass_index >= 25:
            calculated_risk_score += 2

        # ToDo:
        # need to clarify this is it AND or OR
        # should be the average of two readings
        if systolic_blood_pressure >= 140 or diastolic_blood_pressure >= 90:
            calculated_risk_score += 2

        return calculated_risk_score
