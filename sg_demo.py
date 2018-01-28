from OHA.SgFramingham import SgFramingham
from OHA.SingHealth import SingHealth as SHA
from OHA.param_builders.sg_framingham_param_builder import SGFraminghamParamsBuilder as SGFPB

# params = SGFPB().gender('male').age(60).ethnicity('indian').t_chol(4.6, 'mmol/L').hdl_chol(1.8, 'mmol/L').sbp(125)\
#     .smoker(True).diabetic(True).bp_medication(False).build()

params = SGFPB()\
    .gender('m')\
    .age(60)\
    .ethnicity('indian')\
    .t_chol(4.6, 'mmol/L')\
    .hdl_chol(1.8, 'mmol/L')\
    .sbp(125)\
    .smoker()\
    .diabetic(True)\
    .bp_medication(False)\
    .build()

print(params)
result = SgFramingham().calculate(params)
print('--> Sg Framingham:', result)
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
            'gender': 'M',
            'age': 40,
            'ethnicity': 'caucasian',
            'dob': ['computed', '01/10/1987'],
            'occupation': 'office_worker',
            'monthly_income': '',
        },
        'measurements': {
            'height': [1.5, 'm'],
            'weight': [60.0, 'kg'],
            'waist': [99.0, 'cm'],
            'hip': [104.0, 'cm'],
            'sbp': [161, 'sitting'],
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
                'type': 'random', 'units': 'mmol/L', 'value': 5,
            },
            'cholesterol': {
                'type': 'fasting', 'units': 'mmol/L', 'total_chol': 5.2, 'hdl': 1.6, 'ldl': 2.4,
            },
        },
    },
}

print('---- Calculating SingHealth ----')
result = SHA.calculate(input_params)
