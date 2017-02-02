#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import numpy as np
from __helpers import format_params

# ToDo: insert file headers
__author__ = ""
__copyright__ = ""

__license__ = ""
__version__ = ""
__maintainer__ = ""
__email__ = ""


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
        'calc_mean': {'F': 26.1931, 'M': 23.9802}
    }

    # co-efficients used in the calculation. See relevant paper
    @staticmethod
    def __get_co_efficient(key, gender):
        return Framingham.__co_efficients[key][gender]

    @staticmethod
    def calculate_fre_score(params):
        gender = params['gender']
        age = params['age']
        total_cholesterol = params['total_cholesterol']
        hdl_cholesterol = params['hdl_cholesterol']
        on_bp_medication = params['on_bp_medication']
        systolic = params['systolic']
        is_smoker = params['is_smoker']
        has_diabetes = params['has_diabetes']

        risk_chol = (
            Framingham.__get_co_efficient("logAge", gender)
            * np.log(age)
            + Framingham.__get_co_efficient("logTChol", gender)
            * np.log(total_cholesterol)
            - Framingham.__get_co_efficient("logHDLChol", gender)
            * np.log(hdl_cholesterol)
        )

        # If on medication for BP
        if on_bp_medication:
            risk_systolic = (
                Framingham.__get_co_efficient("logSBPRx", gender)
                * np.log(systolic)
            )
        else:
            risk_systolic = (
                Framingham.__get_co_efficient("logSBPNonRx", gender)
                * np.log(systolic)
            )

        risk_smoking = (
            Framingham.__get_co_efficient("logSmoking", gender)
            * is_smoker
        )
        risk_diabetes = (
            Framingham.__get_co_efficient("logDM", gender)
            * has_diabetes
        )
        total_risk = risk_chol + risk_systolic + risk_smoking + risk_diabetes

        framingham_risk_score = 1 - np.power(
            Framingham.__get_co_efficient("so10", gender),
            np.exp(
                total_risk
                - Framingham.__get_co_efficient("calc_mean", gender)
            )
        )

        return framingham_risk_score

    @staticmethod
    def __calculate_heart_age(cvd_risk, gender):

        standard_params = {
            'gender': gender,
            'total_cholesterol': 180,
            'hdl_cholesterol': 45,
            'systolic': 125,
            'on_bp_medication': False,
            'is_smoker': False,
            'has_diabetes': False,
        }

        # run a binary search to estimate heart age
        min_heart_age = 10
        max_heart_age = 200
        suggested_heart_age = (min_heart_age + max_heart_age) / 2

        while min_heart_age <= max_heart_age:
            standard_params['age'] = suggested_heart_age
            age_risk = Framingham.calculate_fre_score(standard_params)

            # print 'age range ->', min_heart_age, max_heart_age, \
            #     '| approx. age:', suggested_heart_age, \
            #     '| age risk:', age_risk, \
            #     '| cvd risk', cvd_risk

            if round(age_risk, 6) == round(cvd_risk, 6):
                break
            elif round(age_risk, 6) > round(cvd_risk, 6):
                max_heart_age = suggested_heart_age - 1
                suggested_heart_age = (min_heart_age + max_heart_age) / 2
            elif round(age_risk, 6) < round(cvd_risk, 6):
                min_heart_age = suggested_heart_age + 1
                suggested_heart_age = (min_heart_age + max_heart_age) / 2

        return suggested_heart_age

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
           ...    'gender':            'M',
           ...    'age':               40,
           ...    'total_cholesterol': 180,
           ...    'hdl_cholesterol':   45,
           ...    'systolic':          125,
           ...    'on_bp_medication':  False,
           ...    'is_smoker':         False,
           ...    'has_diabetes':      False,
           ... }
           >>> Framingham().calculate(params)

        Returns
        -------
        dict
           Framingham risk score and heart age
        """
        params = format_params(params)

        cvd_risk = Framingham.calculate_fre_score(params)
        heart_age = Framingham.__calculate_heart_age(cvd_risk, params['gender'])

        return {
            'cvd_risk': round(cvd_risk, 4),
            'heart_age': heart_age,
        }
