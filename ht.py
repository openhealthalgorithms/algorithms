#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import math
import numpy as np
import os
import sys
import json

from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.HEARTS import HEARTS
from OHA.WHO import WHO
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP
from OHA.Diabetes import Diabetes
from OHA.__assessments import assess_waist_hip_ratio, assess_smoking_status, assess_blood_pressure, assess_bmi, \
    assess_diet, assess_physical_activity
from OHA.__utilities import calculate_bmi
#from DEV.__utilities import load_guidelines, load_guideline_content, output_messages
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder
from OHA.param_builders.who_param_builder import WhoParamsBuilder
#from __helpers import format_params, convert_cholesterol_unit
#from __utilities import calculate_diabetes_risk, calculate_diabetes_status, high_risk_condition_check, assess_diet, assess_physical_activity, assess_bmi, assess_waist_hip_ratio, assess_smoking_status, assess_blood_pressure, estimate_cvd_risk, generate_management_plan, output_messages, load_guidelines, load_guideline_content

"""
Hearts Guideline Outline
By default uses the WHO/ISH risk charts
"""

def calc_cvd_risk(inputParams):
    '''
    Call the relevant WHO model and compute
    '''
    #cvd_risk = (20, '10-20')
    cvd_risk = (40, '30-40')
    return cvd_risk

def main():
    ''' Generates the assessment'''
    
    assessment = {}

    #load guidelines
    #guidelines = load_guidelines('hearts')["body"]

    #load message
    #messages = load_guideline_content()["body"]["messages"]

    #load in the response object
    with open('DEV/request.json') as json_data:
        data = json.load(json_data)
    
    #unpack the request, validate it and set up the params
    demographics    = data['body']['demographics']
    gender          = demographics["gender"]
    measurements    = data['body']['measurements']
    smoking         = data['body']['smoking']
    physical_activity = data['body']['physical_activity']
    diet_history = data['body']['diet_history']
    medical_history = data['body']['medical_history']
    pathology = data['body']['pathology']
    medications = []
    allergies = []

    print('--- Running lifestyle and risk factor assessment ---')
    print(measurements)
    bmi = calculate_bmi(int(measurements['height']), int(measurements['weight']))
    #whr = assess_waist_hip_ratio(measurements['waist'], measurements['hip'], demographics['gender'])

    smoker = assess_smoking_status(smoking)
    print('--- Set smoking status ---')
    #print(messages['smoking'][smoker])
    print(output_messages('smoking', smoker, output_level=4))

    #assess diabetes status or risk
    print('--- Check diabetes status---')
    diabetes_status = calculate_diabetes_status(medical_history, pathology['bsl']['type'], pathology['bsl']['units'], pathology['bsl']['value']) 

    print(diabetes_status)
    #If does not have diabetes
    if diabetes_status['assessment_code'] == 'DM-NONE':
        #calculate diabetes risk score
        diabetes_risk = calculate_diabetes_risk(demographics['gender'], demographics['age'], bmi, whr, measurements['sbp'], measurements['dbp'])
    else:
        #newly diagnosed diabetes, add to existing conditions list
        conditions = medical_history['conditions']
        conditions.append('diabetes')
        medical_history['conditions'] = conditions
        diabetes_risk = "NA"
        #print('diabetes status is %s ' % assessment['diabetes_status'][1])

    diabetes_status['risk'] = diabetes_risk
    assessment['diabetes'] = diabetes_status
    '''assessment['diabetes'] = {
                    'risk' : diabetes_risk,
                    'status' : diabetes_status
                }
            '''
    print('--- High Risk Condition Check ---')
    blood_pressure = {
        'sbp' : measurements['sbp'], 
        'dbp' : measurements['dbp']
    }
    print(blood_pressure)

    bp_assessment = assess_blood_pressure(blood_pressure, medical_history['conditions'], medications)
    assessment['blood_pressure'] = bp_assessment
    '''
    assessment['blood_pressure'] = {
        'bp' : str(measurements['sbp'][0]) + "/" + str(measurements['dbp'][0]),
        'assessment_code' : bp_assessment[0], 
        'assessment' : bp_assessment[1],
        'target' : bp_assessment[2],
        'target_message' : bp_assessment[3]
    }
    '''

    diet = assess_diet(diet_history, medical_history['conditions'])
    
    exercise = assess_physical_activity(physical_activity)
    
    assessment['lifestyle'] = {
        'bmi' : bmi,
        'whr' : whr,
        'diet' : diet,
        'exercise' : exercise,
        'smoking' : smoker
    }

    age = demographics['age']
    #work out how to add in diabetes if newly diagnosed?
    print(medical_history['conditions']) 
    high_risk_condition = high_risk_condition_check(demographics['age'], blood_pressure, medical_history['conditions'])
    print(high_risk_condition)

    assessment['cvd_assessment'] = {
        'high_risk_condition' : high_risk_condition
    }

    #Determine whether eligible for CVD risk assessment
    estimate_cvd_risk_calc = estimate_cvd_risk(age, high_risk_condition)
    #print('high risk output %s ' % assessment['high_risk'][0])
    #if not high_risk_condition[0]:
    if estimate_cvd_risk_calc[0]:
        # if not already at high risk then calculate CVD risk
        print('do cvd check')
        params = FPB().gender(gender).age(age).t_chol(pathology['cholesterol']['total_chol'], pathology['cholesterol']['units']).hdl_chol(pathology['cholesterol']['hdl'], pathology['cholesterol']['units']).sbp(blood_pressure['sbp']).build()
        result = Framingham().calculate(params)
        print('--> Framingham:', result)
        #use the WHO model to do the cvd risk assessment
        #cvd_risk = calc_cvd_risk(assessment)
        #use the key to look up the guidelines output
        assessment['cvd_assessment']['cvd_risk_result'] = cvd_risk
        print(cvd_risk)
        assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk'][cvd_risk[1]]
        #print(guidelines['cvd_risk'][assessment['cvd_risk'][1]])
    else:
        cvd_calc = estimate_cvd_risk_calc[1]
        print(cvd_calc)
        #assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk']['Refer']

    #finally management advice
    assessment['management'] = generate_management_plan(age, demographics['gender'], medical_history['conditions'], medications, allergies, assessment['cvd_assessment']['guidelines'])
    print("--- Writing Your Results ----")
    with open('response.json', 'w') as fp:
        json.dump(assessment, fp)


if __name__ == "__main__":
    print('---Starting Hearts Assessment----')
    main()

    