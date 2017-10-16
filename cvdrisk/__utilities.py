#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

import json
# Replace this as a module with accessor methods
from __helpers import calculate_bmi, calculate_waist_hip_ratio

global targets

targets = {
    'general' : {
        'active_time' : 150,
        'fruit' : 2,
        'vegetables' : 5,
        'sbp' : 140,
        'dbp' : 90,
    },
    'diabetes' : {
        'sbp' : 130,
        'dbp' : 80,
        'soft_drinks' : 0
    },
    'hypertension' : {
        'sbp' : 120,
        'dbp' : 80,
        'added_salt' : 0,
    }
}

# if dob object passed in then return age
def calculate_age(object):

    return None

def assess_smoking_status(smoking):

    if smoking['current'] == 1:
        return (True, 'SM-R', "Current Smoker")
    elif ((smoking['ex_smoker']) & (smoking['quit_within_year'])):
        return (True, 'SM-A-1', "Ex-smoker, Quit within the year")
    elif ((smoking['ex_smoker'])):
        return (False, 'SM-A-2', "Ex-smoker, Quit more than a year ago")
    else:
        return (False, 'SM-G', "Non-smoker")

def assess_waist_hip_ratio(waist, hip, gender):
    whr = calculate_waist_hip_ratio(waist[0], hip[0])
    if gender == "F":
        if whr >= 0.85:
            return (True, whr, "High WHR")
        else:
            return (False, whr, "Normal WHR")
    if gender == "M":
        if whr >= 0.9:
            return (True, whr, "High WHR")
        else:
            return (False, whr, "Normal WHR")

def assess_bmi(height, weight):
    bmi = calculate_bmi(height[0], weight[0])
    if bmi < 18.5:
        return (True, bmi, "Underweight")
    elif bmi < 25:
        return (False, bmi, "Ideal weight range")
    elif bmi < 30:
        return (True, bmi, "Overweight")
    else:
        return (True, bmi, "Obese")
    return bmi

def assess_physical_activity(active_time):

    if active_time >= targets['general']['active_time']:
        return (True, "on_target")
    else:
        return (False, "off_target")

def assess_diet(diet_history):
    
    if ((diet_history['fruit'] < targets['general']['fruit']) and (diet_history['veg'] < targets['general']['vegetables'])):
        return (False, "low" ,"Fruit & Vegetables targets not being met")
    elif ((diet_history['fruit'] < targets['general']['fruit']) and (diet_history['veg'] >= targets['general']['vegetables'])):
        return (False, "mod", "Fruit targets not met, Good work on the veg!")
    elif ((diet_history['fruit'] > targets['general']['fruit']) and (diet_history['veg'] < targets['general']['vegetables'])):
        return (False, "mod", "Veg targets not met, Good work on the fruit!")
    else:
        return (True, "high", "Great work, Fruit & Veg targets being met")

def assess_blood_pressure(bp, conditions):

    if bp['sbp'] > 160:
        return None

'''
Known heart disease, stroke, transient ischemic attack, DM, kidney disease 
(for assessment, if this has not been done)
Replace these with a lookup table based on concepts (SNOMED or other)
Could also integrate with lexigram.io
'''
def high_risk_condition_check(age, blood_pressure, conditions):

    # Known heart disease, stroke, transient ischemic attack, DM, kidney disease (for assessment, if this has not been done)    
    high_risk_conditions = ['CAD', 'AMI', 'HEART ATTACK', 'CVA', 'TIA', 'STROKE', 'CKD', 'PVD']
    # Return whether medical history contains any of these
    for condition in conditions:
        if condition.upper() in high_risk_conditions:
            return (True, 'Has High Risk Condition %s' % condition.upper())

    #check for other high risk states such as BP > 160 and age > 60 + diabetes (including newly suggested)
    #if (assessment[])
    #blood pressure [value, observation_type]
    sbp = blood_pressure['sbp'][0]
    dbp = blood_pressure['dbp'][0]
    if ((sbp > 200) or (dbp > 120)):
        return (True, 'Severely high blood pressure. Emergency check')
    elif ((age < 40) and ((sbp >= 140) or (dbp >= 90))):
        return (True, 'High blood pressure in under 40, shold be investigated for secondary htn')
    '''
    Go through the guidelines and pull out the rules
    New chest pain .. capture via history?
    Target organ damage based on physical exam
    Cardiac murmurs
    Raised BP ≥140/90 ( in DM above 130/ 80mmHg) while on treatment with 2 or 3 agents
    Any proteinuria
    Newly diagnosed DM with urine ketones 2+ or in lean persons of <30 years
    Total cholesterol >8mmol/l
    DM with poor control despite maximal metformin with or without sulphonylurea
    DM with severe infection and/or foot ulcers
    DM with recent deterioration of vision or no eye exam in 2 years
    High cardiovascular risk
    '''
    return (False, "NO high risk condition, For CVD risk assessment")

def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):

    # move to a helper function
    if bsl_units == 'mg/dl':
        bsl_value = round(float(bsl_value)/18, 1)
 
    for condition in conditions:
        if condition == "diabetes":
            return True
        else:
            if bsl_type == "random":
                if bsl_value >= 11.1:
                    return (True, "BSL-R", "Looks like newly diagnosed diabates")
                elif bsl_value > 7:
                    return (False, "BSL-A", "You are at risk of developing diabetes")
                else:
                    return (False, "BSL-G", "Blood sugar normal")
        return False

def calculate_diabetes_risk(gender, age, bmi, whr, sbp, dbp):

    risk_score = 0
    
    if gender == "M":
        risk_score = risk_score + 2
        if whr >= 0.9:
            risk_score = risk_score + 5
    else:
        if whr >= 0.8:
            risk_score = risk_score + 5
        
    if ((age > 30) & (age < 41)):
        risk_score = risk_score + 3
    elif age > 40:
        risk_score = risk_score + 4
    
    if bmi >= 25:
        risk_score = risk_score + 2
        
    # need to clarify this is it & or OR
    #  should be the average of two readings
    if ((sbp >= 140) or (dbp >= 90)):
        risk_score = risk_score + 2
    
    return risk_score

def generate_management_plan(assessment):
    '''
    Calculate the specific targets, management advice, follow up, referrals based on the assessment
    General lifestyle
        - BMI & WHR
        - diet
        - exercise
    Smoking
    CVD Risk
    Blood Pressure
        - manage as per cvd risk unless very high
    Cholesterol
        - manage as per cvd risk unless very high
    '''
    management = {}


    return None


