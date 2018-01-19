#!/usr/bin/env python
#  -*- coding: utf-8 -*-

def calculate_bmi(weight, height):
    body_mass_index = round(float(weight / (height * height)), 2)
    return body_mass_index


def calculate_waist_hip_ratio(waist, hip):
    waist_hip_ratio = round(float(waist / hip), 2)
    return waist_hip_ratio


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

'''
def calculate_caloric_intake(gender, weight, height, age, physical_activity_level):
    
        Using the Revised Harris-Benedict Equation 
        Men BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) - (5.677 x age in years)
        Women BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) - (4.330 x age in years)

   
    # ensure the height, weight are in the correct units
    # currently assuming so

    if gender == "M":
        bmr = 88.362 + (13.397 * weight) + (4.7999 * height) - (5.677 * age)
    elif gender == "F":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)        

    # apply physical activity level
    # mutiply by
    # level = 0 = sedentary / little to no exercise
    #           => Daily kilocalories needed = BMR x 1.2
    # level = 1 = light exercise (1-3 days per week)
    #           => Daily kilocalories needed = BMR x 1.375
    # level = 2 = moderate exercise (3–5 days per week)
    #            => Daily kilocalories needed = BMR x 1.55
    # level = 3 = heavy exercise (6–7 days per week)
    #           => Daily kilocalories needed = BMR x 1.725
    # level = 4 = very heavy exercise (twice per day, extra heavy workouts)
    #           => Daily kilocalories needed = BMR x 1.9
    
    activity_multiplier = 1.0

    if physical_activity_level == 0:
        activity_multiplier = 1.2
    elif physical_activity_level == 1:
        activity_multiplier = 1.375
    elif physical_activity_level == 2:
        activity_multiplier = 1.55
    elif physical_activity_level == 3:
        activity_multiplier = 1.725
    elif physical_activity_level == 4:
        activity_multiplier = 1.9

    caloric_intake = bmr*activity_multiplier

    return caloric_intake

'''
