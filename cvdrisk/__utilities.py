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
        'activity_type' : 'moderate',
        'fruit' : 2,
        'vegetables' : 5,
        'sbp' : 140,
        'dbp' : 90,
    },
    'diabetes' : {
        'sbp' : 130,
        'dbp' : 80,
        'soft_drinks' : 0,
        'added_sugar' : 0,
        'added_salt' : 0
    },
    'hypertension' : {
        'sbp' : 120,
        'dbp' : 80,
        'added_salt' : 0,
    }
}

def has_condition(c, conditions):
    
    has_condition = False
    
    for condition in conditions:
        if condition == c:
            has_condition = True

    return has_condition

# if dob object passed in then return age
def calculate_age(object):

    return None

def assess_smoking_status(smoking):

    _assessment = ""
    _assessment_code = ""
    _target = 0
    _target_message = "No smoking"

    if smoking['current'] == 1:
        _value = 1
        _assessment = "Current Smoker"
        _assessment_code = "SM-R"
        #return (True, 'RED', 'SM-R', "Current Smoker")
    elif ((smoking['ex_smoker']) & (smoking['quit_within_year'])):
        _value = 1
        _assessment = "Ex-smoker, Quit within the year"
        _assessment_code = "SM-A-1"
        #return (True, 'AMBER', 'SM-A-1', "Ex-smoker, Quit within the year")
    elif ((smoking['ex_smoker'])):
        _value = 0
        _assessment = "Ex-smoker, Quit more than a year ago"
        _assessment_code = "SM-A-2"
        #return (False, 'YELLOW', 'SM-A-2', "Ex-smoker, Quit more than a year ago")
    else:
        _value = 0
        _assessment = "Non-Smoker"
        _assessment_code = "SM-G"
        #return (False, 'GREEN', 'SM-G', "Non-smoker")
    
    smoking_output = {
        'value' : _value,
        'assessment_code' : _assessment_code,
        'target' : _target,
        'target_message' : _target_message
    }

    return smoking_output
        

def assess_waist_hip_ratio(waist, hip, gender):

    _assessment = ""
    _assessment_code = ""
    _target = ""
    _target_message = ""

    whr = calculate_waist_hip_ratio(waist[0], hip[0])
    if gender == "F":
        _target = 0.85
        _target_message = "WHR for women is < 0.85"
        if whr >= 0.85:
            _assessment = True
            _assessment_code = "WHR-H"
            #return (True, 'AMBER', "WHR-H", whr, '<0.85')
        else:
            _assessment = False
            _assessment_code = "WHR-N"
            #return (False, 'GREEN', "WHR-N", whr, '<0.85')
    if gender == "M":
        _target = 0.9
        _target_message = "WHR for men is < 0.9"
        if whr >= 0.9:
            _assessment = True
            _assessment_code = "WHR-H"
            #return (True, 'AMBER', "WHR-H", whr, '<0.9')
        else:
            _assessment = False
            _assessment_code = "WHR-N"
            #return (False, 'GREEN', "WHR-N", whr, '<0.9')
            
    whr_output = {
        'value' : whr,
        'assessment_code' : _assessment_code,
        'target' : _target,
        'target_message' : _target_message
    }

    return whr_output

def assess_bmi(height, weight):

    _assessment = ""
    _assessment_code = ""
    _target = "18.5 - 24.9"
    _target_message = ""

    bmi = calculate_bmi(height[0], weight[0])

    if bmi < 18.5:
        _assessment = True
        _assessment_code = "UW"
        #return (True, 'AMBER', 'UW', bmi)
    elif bmi < 25:
        _assessment = False
        _assessment_code = "NW"
        #return (False, 'GREEN', 'NW', bmi)
    elif bmi < 30:
        _assessment = True
        _assessment_code = "OW"
        #return (True, 'AMBER', 'OW', bmi)
    else:
        _assessment = True
        _assessment_code = "OB"
        #return (True, 'RED', 'OB', bmi)
    #return bmi

    bmi_output = {
        'value' : bmi,
        'assessment_code' : _assessment_code,
        'target' : _target,
        'target_message' : _target_message
    }

    return bmi_output

def assess_physical_activity(active_time):

    _assessment = ""
    _assessment_code = ""
    _target = ""
    _target_message = ""

    if active_time >= targets['general']['active_time']:
        _assessment = "ON TARGET"
        _assessment_code = ""
        _target = ""
        _target_message = "> 150 minutes weekly"
        #return (True, 'GREEN', "on_target")
    else:
        #return (False, 'AMBER', "off_target")
        _assessment = "OFF TARGET"
        _assessment_code = ""
        _target = ""
        _target_message = "> 150 minutes weekly"

    pa_output = {
        'value' : active_time,
        'assessment_code' : _assessment_code,
        'target' : _target,
        'target_message' : _target_message
    }

    return pa_output

def assess_diet(diet_history, conditions):

    _assessment = ""
    _assessment_code = ""
    _target = ""
    _target_message = ""
    '''
    General Rules:
    - Aim for 50% frit & vegetables (with specific targets for F&V), 25% lean protein, 25% carbohydrates
    - Minimise amount of fast foods, processed foods
    - Replace soda with non-sugary alternatives
    - Limit amount of added salt & sugar - for diabetics and hypertensives, target is 0
    - If trying to lose weight, avoid hotel or fast food (not sure what is in them)
    - For diabetes:
        - no added sugar
        - If BMI > 25, aim for weight loss of 600-700 calories per day
    - For Hypertensive:
        - no added salt
    Step 1: Assess general diet, fruits & vegetables based on targets (2 fruits & 5 vegetables per day)
    Step 2: Proportion of carbohydrates - should be 25% (other 25% lean protein, 50% vegetables, salads)
    Step 3: Amount of soda or other added sugars
    '''
    if has_condition('diabetes', conditions):
        diabetes = True
        
    if has_condition('hypertension', conditions):
        htn = True

    if ((diet_history['fruit'] < targets['general']['fruit']) 
        and (diet_history['veg'] < targets['general']['vegetables'])):

        _assessment = "BOTH OFF TARGET"
        _assessment_code = 0
        _target = ""
        _target_message = ""

        #return (False, 'RED', 'Fruit & Vegetables targets not being met')
    
    elif ((diet_history['fruit'] < targets['general']['fruit']) 
        and (diet_history['veg'] >= targets['general']['vegetables'])):
        
        _assessment = "PARTIAL OFF TARGET"
        _assessment_code = 1
        _target = ""
        _target_message = "Two serves of fruit and 5 serves of vegetables"

        #return (False, 'AMBER', "Fruit targets not met, Good work on the veg!")
    
    elif ((diet_history['fruit'] > targets['general']['fruit']) 
        and (diet_history['veg'] < targets['general']['vegetables'])):
        
        _assessment = "PARTIAL OFF TARGET"
        _assessment_code = 2
        _target = ""
        _target_message = "Two serves of fruit and 5 serves of vegetables"

        #return (False, 'AMBER', "Veg targets not met, Good work on the fruit!")
    
    else:
    
        _assessment = "ON TARGET"
        _assessment_code = 3
        _target = ""
        _target_message = "Two serves of fruit and 5 serves of vegetables"
        #return (True, 'RED', "Great work, Fruit & Veg targets being met")
    
    diet_output = {
        'values' : {
            'fruit' : diet_history['fruit'],
            'vegetables' : diet_history['veg']
        },
        'assessment_code' :_assessment_code, 
        'assessment' :_assessment,
        'target' : {
            'fruit' : targets['general']['fruit'],
            'vegetables' : targets['general']['vegetables']
        },
        'target_message' : _target_message
    }

    return diet_output
        
def assess_blood_pressure(bp, conditions, medications):

    _assessment = ""
    _assessment_code = ""
    _target = ""
    _target_message = ""
    #returns: 
    #"assessment": "blood pressure off target",
    #"assessment_code" : ""
    #"bp": "145/91",
    #"target": 130,
    #"target_message": "target set for patient with diabetes"
    bp_output = {}
    
    _sbp = bp['sbp'][0]
    _dbp = bp['dbp'][0]

    if _sbp > 160:
        _assessment = "HIGH RISK"
        _assessment_code = "BP-HR-0"
        _target_message = "Blood pressure is at high risk level. Seek Care"
        #return('BP-HR-0', 'blood pressure is at high risk level', _sbp, 120)

    #if on medications and sbp > 140
    # check diabetes status
    elif has_condition('diabetes', conditions):
        if _sbp > 130:
            _assessment = "OFF TARGET"
            _assessment_code = "BP-DM-0"
            _target = 130
            _target_message = "Target set for patient with diabetes"
            #return('BP-DM-0', 'OFF TARGET', _sbp, 130, 'target set for patient with diabetes')
        else:
            _assessment = "ON TARGET"
            _assessment_code = "BP-DM-1"
            _target = 130
            _target_message = "Target set for patient with diabetes"
            #return('BP-DM-1', 'ON TARGET', _sbp, 130,  'target set for patient with diabetes')
    elif ((sbp < 140) and (sbp >= 120)):
        _assessment = "OFF TARGET, MILD"
        _assessment_code = "BP-NoHx-0"
        _target = 120
        _target_message = "Target set for patient with no history or medications"
        #return('BP-NoHx-0', 'OFF TARGET, MILD', _sbp, 120,  'target set for patient with no history or medications')
    elif sbp > 140:
        _assessment = "OFF TARGET, ELEVATED"
        _assessment_code = "BP-NoHx-1"
        _target = 120
        _target_message = "Target set for patient with no history or medications"
        
        #return('BP-NoHx-1', 'OFF TARGET, ELEVATED', _sbp, 120, 'target set for patient with no history or medications')
    
    bp_output = {
        'bp' : str(_sbp) + "/" + str(_dbp),
        'assessment_code' :_assessment_code, 
        'assessment' :_assessment,
        'target' : _target,
        'target_message' : _target_message
    }
    return bp_output

'''
Known heart disease, stroke, transient ischemic attack, DM, kidney disease 
(for assessment, if this has not been done)
Replace these with a lookup table based on concepts (SNOMED or other)
Could also integrate with lexigram.io
'''
def high_risk_condition_check(age, blood_pressure, conditions):

    _assessment = ""
    _assessment_code = ""
    _target = ""
    _target_message = ""

    # Known heart disease, stroke, transient ischemic attack, DM, kidney disease (for assessment, if this has not been done)    
    high_risk_conditions = ['CVD', 'CAD', 'AMI', 'HEART ATTACK', 'CVA', 'TIA', 'STROKE', 'CKD', 'PVD']
    # Return whether medical history contains any of these
    
    for condition in conditions:
        print(condition)
        if condition.upper() in high_risk_conditions:
            #_assessment = True
            #_assessment_message = 'Has High Risk Condition %s' % condition.upper()
            #_assessment_code = ""
            return (True, 'Has High Risk Condition %s' % condition.upper())

    #check for other high risk states such as BP > 160 and age > 60 + diabetes (including newly suggested)
    #if (assessment[])
    #blood pressure [value, observation_type]
    sbp = blood_pressure['sbp'][0]
    dbp = blood_pressure['dbp'][0]

    if ((sbp > 200) or (dbp > 120)):
        #_assessment = True
        #_assessment_code = "HRC-HTN"
        return (True, "HRC-HTN", 'Severely high blood pressure. Seek emergency care immediately')
    elif ((age < 40) and ((sbp >= 140) or (dbp >= 90))):
        #_assessment = True
        #_assessment_code = "HRC-AGE-BP"
        return (True, "HRC-AGE-BP", 'High blood pressure in under 40, should be investigated for secondary hypertension')
    else:
        #_assessment = False
        #_assessment = "No High Risk Condition"
        return(False, "No High Risk Condition") 
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
    #return (False, "NO high risk condition. Continue for CVD risk assessment")
    
    """hrc_output = {
                    'value' : _assessment,
                    'assessment' : _assessment,
                    'assessment_code' : _assessment_code,
                    'target' : _target,
                    'target_message' : _target_message
                }
            
                print(hrc_output)
            
                return hrc_output
            """
def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):

    #"assessment": "blood pressure off target",
    #assessment_message
    #"assessment_code" : ""
    #"bp": "145/91",
    #"target": 130,
    #"target_message": "target set for patient with diabetes"

    _assessment = ""
    _assessment_code = ""
    _assessment_message = ""
    _target = ""
    _target_message = ""

    diabetes_data = {}
    # move to a helper function
    if bsl_units == 'mg/dl':
        bsl_value = round(float(bsl_value)/18, 1)
 
    for condition in conditions:
        if condition == "diabetes":
            #return True
            _assessment = True
            _assessment_message = "History of Diabetes"
            _assessment_code = 'BSL-R'
            _target = '',
            _target_message = ''
        else:
            if bsl_type == "random":
                if bsl_value >= 11.1:
                    _assessment = True
                    _assessment_message = "Looks like newly diagnosed diabetes"
                    _assessment_code = 'DM-NEW'
                    _target = ''
                    _target_message = ''
                    #diabetes_data['dx'] = True
                    #diabetes_data['diagnosis_type'] = 'DM-New'
                    #diabetes_data['code'] = 'BSL-R' 
                    #return (diabetes_data, "Looks like newly diagnosed diabetes")
                elif bsl_value > 7:
                    _assessment = False
                    _assessment_message = "You are at risk of developing Diabetes"
                    _assessment_code = 'DM-PRE'
                    _target = ''
                    _target_message = ''
                    #diabetes_data['dx'] = False
                    #diabetes_data['diagnosis_type'] = 'DM-Pre'
                    #diabetes_data['code'] = 'BSL-A' 
                    #return (diabetes_data, "You are at risk of developing diabetes")
                else:
                    _assessment = False
                    _assessment_message = "Normal Blood Sugar. No Diabetes"
                    _assessment_code = 'DM-NONE'
                    _target = ''
                    _target_message = ''
                    #diabetes_data['dx'] = False
                    #diabetes_data['diagnosis_type'] = 'DM-NA'
                    #diabetes_data['code'] = 'BSL-G' 
                    #return (diabetes_data, "BSL-G", "Blood sugar normal")
        #return False
        diabetes_output = {
            'value' : bsl_value,
            'assessment' : _assessment,
            'assessment_code' : _assessment_code,
            'assessment_message' : _assessment_message,
            'target' : _target,
            'target_message' : _target_message
        }
        
        return diabetes_output

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

def estimate_cvd_risk(age, high_risk_condition):
    #If age > assessment_age and NO high risk conditions
    assessment_age = 40

    if age < assessment_age:
        return (False, "Not for CVD Risk as Age < 40")
    elif high_risk_condition[0]:
        return (False, "Has High Risk Condition")
    else:
        return (True, "Continue")
    
def calculate_openhealth_score():

    '''
    Generate a score based on:
    Diet
    Exercise
    CVD Risk
    Blood Pressure
    Diabetes
    '''

def prescribe_medications(age, gender, assessment):

    if 'Blood Pressure' in assessment['advice']:
        print('manage blood pressure')

    return None

def generate_management_plan(age, gender, conditions, medications, allergies, assessment):
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
    rx_guidelines = {}

    if 'Blood Pressure' in assessment['advice']:
        print('managing blood pressure')
        # Check existing medications against a list, for now assume none
        # Should check to see that serum Cr and K have been checked
        if age < 55:
            # need to also check for women of child bearing age .. use a beta-blocker not ACE-I
            if gender == "F" and age > 16 and age < 45:
                bp_rx = {
                    'message' : 'Recommend to start first line antihypertensive for woman in child bearing age',
                    'medication' : 'Beta-blocker and/or thiazide diuretic',
                    'warnings' : 'If age < 40, ensure assessment for secondary causes of hypertension',
                    'side_effects' : ''
                }
            elif "ace-i" not in allergies:
                bp_rx = {
                    'message' : 'Recommend to start first line antihypertensive for age < 55 with no allergies',
                    'medication' : 'Thiazide diuretic and/or ACE-I',
                    'warnings' : 'If prescribing ACE-I or A2RB, Test serum creatinine and potassium',
                    'side_effects' : ''
                }
            else:
                bp_rx = {
                    'message' : 'Recommend to start antihypertensive. Allergy to ACE-I identified',
                    'medication' : 'Beta-blocker and/or thiazide diuretic',
                    'warnings' : '',
                    'side_effects' : ''
                }
        elif age > 55:
            bp_rx = {
                'message' : 'Recommend to start first line antihypertensive for age > 55 with no allergies',
                'medication' : 'Calcium Channel Blocker and/or thiazide diuretic',
                'warnings' : '',
                'side_effects' : ''
            }

    rx_guidelines = {
        'BP': bp_rx
    }

    print(rx_guidelines)

    return rx_guidelines


