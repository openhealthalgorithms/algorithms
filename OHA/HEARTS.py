#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import json

import os

from OHA.Defaults import Defaults
from OHA.Diabetes import Diabetes
from OHA.WHO import WHO
from OHA.assessments.BMIAssessment import BMIAssessment
from OHA.assessments.BPAssessment import BPAssessment
from OHA.assessments.DiabetesAssessment import DiabetesAssessment
from OHA.assessments.DietAssessment import DietAssessment
from OHA.assessments.HighRiskConditionAssessment import HighRiskConditionAssessment
from OHA.assessments.PhysicalActivityAssessment import PhysicalActivityAssessment
from OHA.assessments.SmokingAssessment import SmokingAssessment
from OHA.assessments.WHRAssessment import WHRAssessment
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder
from OHA.param_builders.who_param_builder import WhoParamsBuilder

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class HEARTS(object):
    """

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
        filename = 'guideline_hearts_content.json'
        file_path = ('%s/guideline/%s' % (
            os.path.dirname(os.path.realpath(__file__)),
            filename,
        ))
        with open(file_path) as json_data:
            data = json.load(json_data)

        return data['body']['messages']

    @staticmethod
    def load_guidelines(guideline_key):
        filename = 'guideline_%s.json' % guideline_key
        file_path = ('%s/guideline/%s' % (
            os.path.dirname(os.path.realpath(__file__)),
            filename,
        ))
        with open(file_path) as json_data:
            data = json.load(json_data)

        return data

    # should be moved into a package
    @staticmethod
    def output_messages(section, code, output_level):
        # how do we check if this is already in memory?
        messages = HEARTS.load_messages()
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
    def high_risk_condition_check(age, blood_pressure, conditions, high_risk_conditions):
        raise NotImplementedError('Use "HighRiskConditionAssessment"')

    @staticmethod
    def calculate(params):
        assessment = {}
        output_level = 4

        # load guidelines
        guidelines = HEARTS.load_guidelines('hearts')['body']
        # unpack some of the configurations
        # List of high risk conditions
        # Should also get the targets from here
        high_risk_conditions = guidelines['high_risk_conditions']
        targets = guidelines['targets']

        # unpack the request, validate it and set up the params
        region = params['body']['region'] if 'region' in params['body'].keys() else Defaults.region

        demographics = params['body']['demographics']
        measurements = params['body']['measurements']
        smoking = params['body']['smoking']
        physical_activity = params['body']['physical_activity']
        diet_history = params['body']['diet_history']
        medical_history = params['body']['medical_history']
        pathology = params['body']['pathology']
        BMIA = BMIAssessment({'weight': measurements['weight'], 'height': measurements['height']})
        bmi = BMIA.assess()
        bmi['output'] = HEARTS.output_messages('anthro', bmi['code'], output_level)

        WHRA = WHRAssessment(dict(waist=measurements['waist'], hip=measurements['hip'], gender=demographics['gender']))
        whr = WHRA.assess()
        whr['output'] = HEARTS.output_messages('anthro', whr['code'], output_level)

        SMA = SmokingAssessment({'smoking': smoking})
        smoker = SMA.assess()
        smoker['output'] = HEARTS.output_messages('smoking', smoker['code'], output_level)

        # bmi = assess_bmi(calculate_bmi(measurements['weight'][0], measurements['height'][0]))
        # whr = assess_waist_hip_ratio(measurements['waist'], measurements['hip'], demographics['gender'])
        # smoker = assess_smoking_status(smoking)

        # assess diabetes status or risk
        DSA = DiabetesAssessment({
            'conditions': medical_history,
            'bsl_type': pathology['bsl']['type'],
            'bsl_units': pathology['bsl']['units'],
            'bsl_value': pathology['bsl']['value'],
        })
        diabetes_status = DSA.assess()

        # If does not have diabetes
        if not diabetes_status['status']:
            # calculate diabetes risk score
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
            # newly diagnosed diabetes, add to existing conditions list
            conditions = medical_history['conditions']
            conditions.append('diabetes')
            medical_history['conditions'] = conditions
            diabetes_risk = None

        diabetes_status['output'] = HEARTS.output_messages('diabetes', diabetes_status['code'], output_level)
        print(diabetes_status)
        assessment['diabetes'] = diabetes_status

        blood_pressure = {
            'sbp': measurements['sbp'],
            'dbp': measurements['dbp'],
        }

        BPA = BPAssessment({'bp': blood_pressure, 'conditions': medical_history['conditions']})
        bp_assessment = BPA.assess()
        assessment['blood_pressure'] = bp_assessment

        DTA = DietAssessment({'diet_history': diet_history, 'targets': targets})
        diet = DTA.assess()

        PAA = PhysicalActivityAssessment({
            'active_time': physical_activity,
            'targets_active_time': targets['general']['physical_activity']['active_time'],
        })
        exercise = PAA.assess()
        assessment['lifestyle'] = {
            'bmi': bmi,
            'whr': whr,
            'diet': diet,
            'exercise': exercise,
            'smoking': smoker,
        }

        age = demographics['age']
        HRCA = HighRiskConditionAssessment({
            'age': age,
            'bp': blood_pressure,
            'conditions': medical_history['conditions'],
            'hrc': high_risk_conditions,
        })
        has_high_risk_condition = HRCA.assess()

        assessment['cvd_assessment'] = {
            'high_risk_condition': has_high_risk_condition,
        }

        # Determine whether eligible for CVD risk assessment
        estimate_cvd_risk_calc = HEARTS.estimate_cvd_risk(age, has_high_risk_condition)

        if estimate_cvd_risk_calc[0]:

            if smoking['current'] == 0:
                is_smoker = False
            else:
                is_smoker = True

            cvd_params = WhoParamsBuilder() \
                .gender(demographics['gender']) \
                .age(age) \
                .sbp1(blood_pressure['sbp'][0]) \
                .sbp2(blood_pressure['sbp'][0]) \
                .chol(pathology['cholesterol']['total_chol'], pathology['cholesterol']['units']) \
                .smoker(is_smoker) \
                .region(region) \
                .diabetic(diabetes_status['status']) \
                .build()
            cvd_risk = WHO.calculate(cvd_params)
            assessment['cvd_assessment']['cvd_risk_result'] = cvd_risk
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk'][cvd_risk['risk_range']]
        else:
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk']['Refer']

        return assessment

    @staticmethod
    def get_messages():
        return HEARTS.load_messages()

    @staticmethod
    def get_sample_params():
        return dict(
            request=dict(
                api_key='API_KEY',
                api_secret='API_SECRET',
                request_api='https://developers.openhealthalgorithms.org/algos/hearts/',
                country_code='D',
                response_type='COMPLETE',
            ),
            body=dict(
                region='SEARD',
                last_assessment=dict(assessment_date='', cvd_risk='20'),
                demographics=dict(
                    gender='F', age=50, dob=['computed', '01/10/1987'], occupation='office_worker', monthly_income='',
                ),
                measurements=dict(
                    height=[1.5, 'm'], weight=[70.0, 'kg'], waist=[99.0, 'cm'],
                    hip=[104.0, 'cm'], sbp=[145, 'sitting'], dbp=[91, 'sitting'],
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
                    cholesterol=dict(type='fasting', units='mg/dl', total_chol=320, hdl=100, ldl=240),
                ),
            ),
        )
