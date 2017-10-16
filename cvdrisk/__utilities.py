#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
def assess_smoking_status(smoking):

    if smoking['current'] == 1:
        return (True, "current smoker")
    elif ((smoking['ex_smoker']) & (smoking['quit_within_year'])):
        return (True, "ex-smoker, quit within the year")
    else:
        return (False, "non-smoker OR quit over a year ago")

def calculate_waist_hip_ratio(waist, hip):
    whr = waist[0]/hip[0]
    print ("whr %s " % whr)
    return whr

def calculate_bmi(height, weight):
    bmi = weight[0]/(height[0]*height[0])
    print ("BMI is %s " % bmi)
    return bmi

def assess_physical_activity(active_time):

    if active_time >= targets['general']['active_time']:
        return (True, "on_target")
    else:
        return (False, "off_target")

def assess_diet(diet_history):
    print("calculating diet")
    print('diet history is %s ' % diet_history)
    print('targets are %s ' % targets)
    
    if diet_history['fruit'] < targets['general']['fruit']:
        print("Fruit below target")

    if ((diet_history['fruit'] < targets['general']['fruit']) and (diet_history['veg'] < targets['general']['vegetables'])):
        return (False, "low" ,"Fruit & Vegetables targets not being met")
    elif ((diet_history['fruit'] < targets['general']['fruit']) and (diet_history['veg'] >= targets['general']['vegetables'])):
        return (False, "mod", "Fruit targets not met, Good work on the veg!")
    elif ((diet_history['fruit'] > targets['general']['fruit']) and (diet_history['veg'] < targets['general']['vegetables'])):
        return (False, "mod", "Veg targets not met, Good work on the fruit!")
    else:
        print(diet_history['veg'])
        return (True, "high", "Great work, Fruit & Veg targets being met")

'''
Known heart disease, stroke, transient ischemic attack, DM, kidney disease 
(for assessment, if this has not been done)
Replace these with a lookup table based on concepts (SNOMED or other)
Could also integrate with lexigram.io
'''
def high_risk_condition_check(conditions):
    
    high_risk_conditions = ['CAD', 'AMI', 'HEART ATTACK', 'CVA', 'TIA', 'STROKE', 'CKD', 'PVD']
    # Return whether medical history contains any of these
    for condition in conditions:
        if condition.upper() in high_risk_conditions:
            return (True, 'Has High Risk Condition %s' % condition.upper())

    return False

def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):

    if bsl_units == 'mg/dl':
        bsl_value = round(float(bsl_value)/18, 1)
        print('bsl type is %s ' % bsl_type)
        print('bsl value is %s ' % bsl_value)

    for condition in conditions:
        if condition == "diabetes":
            return True
        else:
            if bsl_type == "random":
                if bsl_value >= 11.1:
                    return (True, "new_diagnosis")
                elif bsl_value > 7:
                    return (False, "pre_diabetes")
                else:
                    return (False, "normal")
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
