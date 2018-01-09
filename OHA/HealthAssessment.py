#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import json
import os

from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.HEARTS import HEARTS
from OHA.__assessments import assess_waist_hip_ratio, assess_smoking_status, assess_blood_pressure, assess_bmi, \
    assess_diet, assess_physical_activity
from OHA.__utilities import calculate_bmi
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder


__author__ = 'fredhersch'
__email__ = 'fredhersch@gmail.com'


class HealthAssessment(object):
    """
        General Health Assessment
    """

    @staticmethod
    def estimate_cvd_risk(age, high_risk_condition):
        # If age > assessment_age and NO high risk conditions
        assessment_age = 40

        if age < assessment_age:
            return False, "Not for CVD Risk as Age < 40"
        elif high_risk_condition[0]:
            return False, "Has High Risk Condition"
        else:
            return True, "Continue"

    @staticmethod
    def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):
        _assessment = ""
        _assessment_code = ""
        _target = ""

        # move to a helper function
        if bsl_units == 'mg/dl':
            bsl_value = round(float(bsl_value) / 18, 1)

        for condition in conditions:
            if condition == "diabetes":
                _assessment = True
                _assessment_code = 'BSL-R'
                _target = ''
            else:
                if bsl_type == "random":
                    if bsl_value > 11:
                        _assessment = True
                        _assessment_code = 'DM-NEW'
                        _target = ''
                    elif bsl_value > 7:
                        _assessment = False
                        _assessment_code = 'DM-PRE'
                        _target = ''
                    else:
                        _assessment = False
                        _assessment_code = 'DM-NONE'
                        _target = ''
            # return False
            diabetes_output = {
                'value': bsl_value,
                'assessment': _assessment,
                'assessment_code': _assessment_code,
                'target': _target,
            }

            return diabetes_output

    @staticmethod
    def load_messages():
        filename = 'guideline_content.json'
        file_path = ('%s/guideline/%s' % (
            os.path.dirname(os.path.realpath(__file__)),
            filename
        ))
        with open(file_path) as json_data:
            data = json.load(json_data)

        return data["body"]["messages"]

    @staticmethod
    def load_guidelines(guideline_key):
        filename = 'guideline_%s.json' % guideline_key
        file_path = ('%s/guideline/%s' % (
            os.path.dirname(os.path.realpath(__file__)),
            filename
        ))
        with open(file_path) as json_data:
            data = json.load(json_data)

        return data

    @staticmethod
    def high_risk_condition_check(age, blood_pressure, conditions):
        # Known heart disease, stroke, transient ischemic attack, DM, kidney disease (for assessment, if this has not
        #  been done)
        high_risk_conditions = ['CVD', 'CAD', 'AMI', 'HEART ATTACK', 'CVA', 'TIA', 'STROKE', 'CKD', 'PVD']
        # Return whether medical history contains any of these

        for condition in conditions:
            if condition.upper() in high_risk_conditions:
                return True, 'Has High Risk Condition %s' % condition.upper()

        # check for other high risk states such as BP > 160 and age > 60 + diabetes (including newly suggested)
        # if (assessment[])
        # blood pressure [value, observation_type]
        sbp = blood_pressure['sbp'][0]
        dbp = blood_pressure['dbp'][0]

        if sbp > 200 or dbp > 120:
            return True, "HRC-HTN", 'Severely high blood pressure. Seek emergency care immediately'
        elif age < 40 and (sbp >= 140 or dbp >= 90):
            return (
                True, "HRC-AGE-BP",
                'High blood pressure in under 40, should be investigated for secondary hypertension')
        else:
            return False, "No High Risk Condition"

    @staticmethod
    def calculate(params):
        assessment = {}

        # load guidelines for SIMPLE algorithm model
        guidelines = HealthAssessment.load_guidelines('health_assessment')["body"]

        # unpack the request, validate it and set up the params
        demographics = params['body']['demographics']
        gender = demographics['gender']
        measurements = params['body']['measurements']
        smoking = params['body']['smoking']
        physical_activity = params['body']['physical_activity']
        diet_history = params['body']['diet_history']
        medical_history = params['body']['medical_history']
        pathology = params['body']['pathology']
        medications = []

        bmi = assess_bmi(calculate_bmi(measurements['weight'][0], measurements['height'][0]))
        whr = assess_waist_hip_ratio(measurements['waist'], measurements['hip'], demographics['gender'])
        smoker = assess_smoking_status(smoking)

        # assess diabetes status or risk
        # // FH these functions should be in a general Assessment class
        diabetes_status = HealthAssessment.calculate_diabetes_status(
            medical_history, pathology['bsl']['type'], pathology['bsl']['units'], pathology['bsl']['value']
        )

        # If does not have diabetes
        if diabetes_status['assessment_code'] == 'DM-NONE':
            # calculate diabetes risk score
            diabetes_params = DiabetesParamsBuilder() \
                .gender(demographics['gender']) \
                .age(demographics['age']) \
                .waist(measurements['waist']) \
                .hip(measurements['hip']) \
                .height(measurements['height']) \
                .weight(measurements['weight']) \
                .sbp(measurements['sbp']) \
                .dbp(measurements['dbp']) \
                .build()
            diabetes_risk = Diabetes().calculate(diabetes_params)['risk']
        else:
            # newly diagnosed diabetes, add to existing conditions list
            conditions = medical_history['conditions']
            conditions.append('diabetes')
            medical_history['conditions'] = conditions
            diabetes_risk = "NA"
            # print('diabetes status is %s ' % assessment['diabetes_status'][1])

        diabetes_status['risk'] = diabetes_risk
        assessment['diabetes'] = diabetes_status
        blood_pressure = {
            'sbp': measurements['sbp'],
            'dbp': measurements['dbp']
        }

        bp_assessment = assess_blood_pressure(blood_pressure, medical_history['conditions'])
        assessment['blood_pressure'] = bp_assessment
        diet = assess_diet(diet_history, medical_history['conditions'])
        exercise = assess_physical_activity(physical_activity)
        assessment['lifestyle'] = {
            'bmi': bmi,
            'whr': whr,
            'diet': diet,
            'exercise': exercise,
            'smoking': smoker
        }

        age = demographics['age']
        # work out how to add in diabetes if newly diagnosed?
        high_risk_condition = HEARTS.high_risk_condition_check(
            demographics['age'], blood_pressure, medical_history['conditions']
        )

        assessment['cvd_assessment'] = {
            'high_risk_condition': high_risk_condition
        }

        # Determine whether eligible for CVD risk assessment
        estimate_cvd_risk_calc = HEARTS.estimate_cvd_risk(age, high_risk_condition)
        # print('high risk output %s ' % assessment['high_risk'][0])
        # if not high_risk_condition[0]:
        if estimate_cvd_risk_calc[0]:
            cvd_params = FraminghamParamsBuilder() \
                .gender(gender) \
                .age(age) \
                .t_chol(pathology['cholesterol']['total_chol'], pathology['cholesterol']['units']) \
                .hdl_chol(pathology['cholesterol']['hdl'], pathology['cholesterol']['units']) \
                .sbp(blood_pressure['sbp'][0]) \
                .build()
            print("cvd params --- %s " % cvd_params)
            fre_result = Framingham().calculate(cvd_params)
            print("--- FRE result %s " % fre_result)
            cvd_risk = round(fre_result['risk'] * 100, 2)
            heart_age = fre_result['heart_age']
            print("cvd risk is %s " % cvd_risk)
            print("heart age is %s " % heart_age)
            risk_range = fre_result['risk_range']
            
            # use the key to look up the guidelines output
            assessment['cvd_assessment']['cvd_risk_result'] = fre_result
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk'][fre_result['risk_range']]
        
        else:
            cvd_calc = estimate_cvd_risk_calc[1]
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk']['Refer']

        return assessment

    @staticmethod
    def get_messages():
        return HEARTS.load_messages()

    @staticmethod
    def get_sample_params():
        return dict(
            request=dict(
                api_key="API_KEY",
                api_secret="API_SECRET",
                request_api="https://developers.openhealthalgorithms.org/algos/hearts/",
                country_code="D",
                response_type="COMPLETE"
            ),
            body=dict(
                last_assessment=dict(assessment_date="", cvd_risk="20"),
                demographics=dict(
                    gender="F", age=50, dob=["computed", "01/10/1987"], occupation="office_worker", monthly_income=""
                ),
                measurements=dict(
                    height=[1.5, "m"], weight=[70.0, "kg"], waist=[99.0, "cm"],
                    hip=[104.0, "cm"], sbp=[145, "sitting"], dbp=[91, "sitting"]
                ),
                smoking=dict(current=0, ex_smoker=1, quit_within_year=0),
                physical_activity="120",
                diet_history=dict(fruit=1, veg=6, rice=2, oil="olive"),
                medical_history=dict(conditions=["asthma", "tuberculosis"]),
                allergies={},
                medications=["anti_hypertensive", "statin", "antiplatelet", "bronchodilator"],
                family_history=["cvd"],
                pathology=dict(
                    bsl=dict(type="random", units="mg/dl", value=180),
                    cholesterol=dict(type="fasting", units="mg/dl", total_chol=320, hdl=100, ldl=240)
                )
            )
        )
