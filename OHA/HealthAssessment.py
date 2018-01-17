#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import json
import os

from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.__assessments import assess_diet, check_medications
from OHA.assessments.BMIAssessment import BMIAssessment
from OHA.assessments.BPAssessment import BPAssessment
from OHA.assessments.DiabetesAssessment import DiabetesAssessment
from OHA.assessments.PhysicalActivityAssessment import PhysicalActivityAssessment
from OHA.assessments.SmokingAssessment import SmokingAssessment
from OHA.assessments.WHRAssessment import WHRAssessment
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
            return False, 'Not for CVD Risk as Age < 40'
        elif high_risk_condition['status']:
            return False, 'Has High Risk Condition'
        else:
            return True, 'Continue'

    @staticmethod
    def load_messages():
        filename = 'guideline_healthassessment_content.json'
        file_path = ('%s/guideline/%s' % (
            os.path.dirname(os.path.realpath(__file__)),
            filename
        ))
        with open(file_path) as json_data:
            data = json.load(json_data)

        return data['body']['messages']

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
    def high_risk_condition_check(age, blood_pressure, conditions, high_risk_conditions):
        # Known heart disease, stroke, transient ischemic attack, DM, kidney disease (for assessment, if this has not
        # been done)
        # Pull this in from the configuration file
        # high_risk_conditions =
        # Return whether medical history contains any of these
        has_high_risk_condition = False
        result_code = ''

        hrc_value = None
        for condition in conditions:
            if condition.upper() in high_risk_conditions:
                has_high_risk_condition = True
                result_code = 'HR-0'
                hrc_value = condition
            else:
                hrc_value = None

        if not has_high_risk_condition:
            # check for other high risk states such as BP > 160 and age > 60 + diabetes (including newly suggested)
            # if (assessment[])
            # blood pressure [value, observation_type]
            sbp = blood_pressure['sbp'][0]
            dbp = blood_pressure['dbp'][0]

            if sbp > 200 or dbp > 120:
                # return True, 'HRC-HTN', 'Severely high blood pressure. Seek emergency care immediately'
                # Very elevated
                has_high_risk_condition = True
                result_code = 'HR-1'
            elif age < 40 and (sbp >= 140 or dbp >= 90):
                # High blood pressure in under 40, should be investigated for secondary hypertension
                result_code = 'HR-2'

        hrc_output = {
            'status': has_high_risk_condition,
            'reason': hrc_value,
            'code': result_code
        }

        return hrc_output

    @staticmethod
    def output_messages(section, code, output_level):
        # how do we check if this is already in memory?
        messages = HealthAssessment.load_messages()
        output = []

        if output_level == 0:
            output = messages[section][code]
        elif output_level == 1:
            output = messages[section][code][0:1]
        elif output_level == 2:
            output = messages[section][code][0:2]
        elif output_level == 3:
            output = messages[section][code][0:3]
        elif output_level == 4:
            output = messages[section][code][0:4]

        return output

    @staticmethod
    def calculate(params):
        assessment = {}
        output_level = 2

        guidelines = HealthAssessment.load_guidelines('healthassessment')['body']
        high_risk_conditions = guidelines['high_risk_conditions']
        targets = guidelines['targets']

        demographics = params['body']['demographics']
        gender = demographics['gender']
        measurements = params['body']['measurements']
        smoking = params['body']['smoking']
        physical_activity = params['body']['physical_activity']
        diet_history = params['body']['diet_history']
        medical_history = params['body']['medical_history']
        pathology = params['body']['pathology']
        medications = params['body']['medications']

        BMIA = BMIAssessment({'weight': measurements['weight'], 'height': measurements['height']})
        bmi = BMIA.assess()
        bmi['output'] = HealthAssessment.output_messages('anthro', bmi['code'], output_level)

        WHRA = WHRAssessment(dict(waist=measurements['waist'], hip=measurements['hip'], gender=demographics['gender']))
        whr = WHRA.assess()
        whr['output'] = HealthAssessment.output_messages('anthro', whr['code'], output_level)

        SMA = SmokingAssessment({'smoking': smoking})
        smoker = SMA.assess()
        smoker['output'] = HealthAssessment.output_messages('smoking', smoker['code'], output_level)

        DSA = DiabetesAssessment({
            'conditions': medical_history,
            'bsl_type': pathology['bsl']['type'],
            'bsl_units': pathology['bsl']['units'],
            'bsl_value': pathology['bsl']['value']
        })
        diabetes_status = DSA.assess()

        if not diabetes_status['status']:
            diabetes_params = DiabetesParamsBuilder() \
                .gender(demographics['gender']) \
                .age(demographics['age']) \
                .waist(measurements['waist'][0]) \
                .hip(measurements['hip'][0]) \
                .height(measurements['height'][0]) \
                .weight(measurements['weight'][0]) \
                .sbp(measurements['sbp'][0]) \
                .dbp(measurements['dbp'][0]) \
                .build()
            diabetes_risk = Diabetes().calculate(diabetes_params)
            diabetes_status['risk'] = diabetes_risk['risk']
            diabetes_status['code'] = diabetes_risk['code']
        else:
            conditions = medical_history['conditions']
            conditions.append('diabetes')
            medical_history['conditions'] = conditions
            diabetes_risk = None

        diabetes_status['output'] = HealthAssessment.output_messages('diabetes', diabetes_status['code'], output_level)
        assessment['diabetes'] = diabetes_status

        blood_pressure = {
            'sbp': measurements['sbp'],
            'dbp': measurements['dbp']
        }

        BPA = BPAssessment({'bp': blood_pressure, 'conditions': medical_history['conditions']})
        bp_assessment = BPA.assess()
        assessment['blood_pressure'] = bp_assessment
        bp_assessment['output'] = HealthAssessment.output_messages(
            'blood_pressure', bp_assessment['code'], output_level
        )
        assessment['blood_pressure'] = bp_assessment

        diet = assess_diet(diet_history, medical_history['conditions'], targets)
        PAA = PhysicalActivityAssessment(dict(
            active_time=physical_activity,
            targets_active_time=targets['general']['physical_activity']['active_time']
        ))
        exercise = PAA.assess()
        assessment['lifestyle'] = {
            'bmi': bmi,
            'whr': whr,
            'diet': diet,
            'exercise': exercise,
            'smoking': smoker
        }

        age = demographics['age']
        has_high_risk_condition = HealthAssessment.high_risk_condition_check(
            demographics['age'], blood_pressure, medical_history['conditions'], high_risk_conditions
        )

        assessment['cvd_assessment'] = {
            'high_risk_condition': has_high_risk_condition
        }

        estimate_cvd_risk_calc = HealthAssessment.estimate_cvd_risk(age, has_high_risk_condition)
        if estimate_cvd_risk_calc[0]:
            on_bp_meds = check_medications('anti_hypertensive', medications)
            cvd_params = FraminghamParamsBuilder() \
                .gender(gender) \
                .age(age) \
                .t_chol(pathology['cholesterol']['total_chol'], pathology['cholesterol']['units']) \
                .hdl_chol(pathology['cholesterol']['hdl'], pathology['cholesterol']['units']) \
                .sbp(blood_pressure['sbp'][0]) \
                .bp_medication(on_bp_meds) \
                .smoker(smoker['smoking_calc']) \
                .diabetic(diabetes_status['status']) \
                .build()
            fre_result = Framingham().calculate(cvd_params)

            assessment['cvd_assessment']['cvd_risk_result'] = fre_result
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk'][fre_result['risk_range']]

        else:
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk']['Refer']

        return assessment

    @staticmethod
    def get_messages():
        return HealthAssessment.load_messages()

    @staticmethod
    def get_sample_params():
        return dict(
            request=dict(
                api_key='API_KEY',
                api_secret='API_SECRET',
                request_api='https://developers.openhealthalgorithms.org/algos/hearts/',
                country_code='D',
                response_type='COMPLETE'
            ),
            body=dict(
                last_assessment=dict(assessment_date='', cvd_risk='20'),
                demographics=dict(
                    gender='F', age=50, dob=['computed', '01/10/1987'], occupation='office_worker', monthly_income=''
                ),
                measurements=dict(
                    height=[1.5, 'm'], weight=[70.0, 'kg'], waist=[99.0, 'cm'],
                    hip=[104.0, 'cm'], sbp=[145, 'sitting'], dbp=[91, 'sitting']
                ),
                smoking=dict(current=0, ex_smoker=1, quit_within_year=0),
                physical_activity='120',
                diet_history=dict(fruit=1, veg=6, rice=2, oil='olive'),
                medical_history=dict(conditions=['asthma', 'tuberculosis']),
                allergies={},
                medications=['anti_hypertensive', 'statin', 'antiplatelet', 'bronchodilator'],
                family_history=['cvd'],
                pathology=dict(
                    bsl=dict(type='random', units='mg/dl', value=180),
                    cholesterol=dict(type='fasting', units='mg/dl', total_chol=320, hdl=100, ldl=240)
                )
            )
        )
