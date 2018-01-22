import json

from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.SgFramingham import SgFramingham
from OHA.HEARTS import HEARTS
from OHA.HealthAssessment import HealthAssessment as HA
from OHA.WHO import WHO
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB
from OHA.param_builders.sg_framingham_param_builder import SGFraminghamParamsBuilder as SGFPB

print('--- Diabetes Risk Demo ---\n')
params = DBP() \
    .gender('M').age(40).sbp(150).dbp(92).weight(92, 'kg').height(1.5, 'm').waist(50, 'cm').hip(90, 'cm').build()
result = Diabetes().calculate(params)
print('--> Diabetes:', result)
print()

print('--- Framingham Risk Demos ---\n')
params = FPB().gender('M').age(50).t_chol(300, 'mg/dl').hdl_chol(60, 'mg/dl') \
              .sbp(110).smoker(True).diabetic(False).bp_medication(False).build()
result = Framingham().calculate(params)
print('--> Framingham:', result)
print()

params = FPB().gender('F').age(70).t_chol(170, 'mg/dl').hdl_chol(45, 'mg/dl').sbp(125).build()
result = Framingham().calculate(params)
print('--> Framingham:', result)
print()

print('--- WHO/ISH Risk Demos ---\n')
params = WPB().gender("M").age(50).sbp1(120).sbp2(140).chol(5.2, 'mmol/l').region('SEARD').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ', result)
print()

params = WPB().gender('M').age(50).sbp1(150).sbp2(170).chol(7, 'mmol/l').region('AFRD').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ', result)
print()

params = WPB().gender("M").age(50).sbp1(150).sbp2(170).chol(7, 'mmol/l').region('AFRE').smoker(False).diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ', result)
print()

params = WPB().gender('M').age(70).sbp1(130).sbp2(145).chol(270, 'mg/dl').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ', result)
print()

input_params = {
    'request': {
        'api_key': '4325872943oeqitrqet7',
        'api_secret': '3459823jfweureitu',
        'request_api': 'https://developers.openhealthalgorithms.org/algos/hearts/',
        'country_code': 'D',
        'response_type': 'COMPLETE',
    },
    'body': {
        'region': 'SEARD',
        'last_assessment': {
            'assessment_date': '',
            'cvd_risk': '20',
        },
        'demographics': {
            'gender': 'F',
            'age': 55,
            'dob': ['computed', '01/10/1987'],
            'occupation': 'office_worker',
            'monthly_income': '',
        },
        'measurements': {
            'height': [1.5, 'm'],
            'weight': [60.0, 'kg'],
            'waist': [99.0, 'cm'],
            'hip': [104.0, 'cm'],
            'sbp': [140, 'sitting'],
            'dbp': [91, 'sitting'],
        },
        'smoking': {
            'current': 0,
            'ex_smoker': 1,
            'quit_within_year': 0,
        },
        'physical_activity': '120',
        'diet_history': {
            'fruit': 1, 'veg': 6, 'rice': 2, 'oil': 'olive',
        },
        'medical_history': {
            'conditions': ['asthma', 'tuberculosis'],
        },
        'allergies': {},
        'medications': ['anti_hypertensive', 'statin', 'antiplatelet', 'bronchodilator'],
        'family_history': ['diabetes', 'cvd'],
        'pathology': {
            'bsl': {
                'type': 'random', 'units': 'mg/dl', 'value': 180,
            },
            'cholesterol': {
                'type': 'fasting', 'units': 'mg/dl', 'total_chol': 300, 'hdl': 100, 'ldl': 240,
            },
        },
    },
}

print('--- HEARTS Package Demo ---\n')
result = HEARTS().calculate(input_params)
print('--> HEARTS: => ', result)
print()

with open('response_hearts.json', 'w') as fp:
        json.dump(result, fp)

print('--- General Health Assessment using FRE Demo ---\n')
result = HA().calculate(input_params)
print('--> HealthAssessment ALGO: => ', result)
print()

with open('response_healthassessment.json', 'w') as fp:
        json.dump(result, fp)

print(' --- Singapore CVD FRE demo ---\n')
params = SGFPB().gender('male').age(60).ethnicity('indian').t_chol(4.6, 'mmol/L').hdl_chol(1.8, 'mmol/L').sbp(125).smoker(True).diabetic(True).bp_medication(False).build()
result = SgFramingham().calculate(params)
print('--> Sg Framingham:', result)
print()
