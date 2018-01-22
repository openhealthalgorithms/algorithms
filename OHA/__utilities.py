#!/usr/bin/env python
#  -*- coding: utf-8 -*-


def calculate_bmi(weight, height):
    raise NotImplementedError('Use "helpers.measurements.BMI"')


def calculate_waist_hip_ratio(waist, hip):
    raise NotImplementedError('Use "helpers.measurements.WaistHipRatio"')


def cvd_risk_string(cvd_risk):
    if cvd_risk == 10:
        return '<10'
    elif cvd_risk == 20:
        return '10-20'
    elif cvd_risk == 30:
        return '20-30'
    elif cvd_risk == 40:
        return '30-40'
    elif cvd_risk == 50:
        return '>40'
    else:
        return '>40'


def calculate_caloric_intake(gender, weight, height, age, physical_activity_level):
    raise NotImplementedError('Use "helpers.calculators.CaloricIntake"')
