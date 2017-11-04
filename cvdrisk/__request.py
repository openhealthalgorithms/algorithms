request : {
  'api_key' : '4325872943oeqitrqet7' 
  'api_secret' : '3459823jfweureitu' 
  'request_api' : 'https://developers.openhealthalgorithms.org/algos/hearts/'
  'country_code' : 'D'
  'response_type' : 'COMPLETE'
}, 
body : 
{
    last_assessment = {
        'assessment_date' : '',
        'cvd_risk' : '20'
    },
    demographics = {
        'gender' : 'F',
        'age' : 30,
        'dob' : ['computed', '01/10/1987'],
        'occupation' : 'office_worker',
        'monthly_income' : ''
    },
    measurements = {
        'height' : [1.5, 'm'],
        'weight' : [70.0, 'kg'],
        'waist' : [99.0, 'cm'],
        'hip' : [104.0, 'cm'],
        'sbp' : [139, 'sitting'],
        'dbp' : [80, 'sitting']
    },
    smoking = {
        'current' : 0,
        'ex_smoker' : 1,
        'quit_within_year' : 0
    },
    physical_activity = '120', # minutes per week
    diet_history = {
        'fruit' : 1, 'veg' : 6, 'rice' : 2, 'oil' : 'olive'
        },
    medical_history = {
        'conditions' = ['asthma', 'tuberculosis']
    },
    allergies = {},
    medications = ['anti_hypertensive', 'statin', 'antiplatelet', 'bronchodilator'],
    family_history = ['cvd'],
    pathology = {
    	[
        'bsl' = {
            'type' : 'random', 'units' : 'mg/dl', 'value' : 240
        }
    	],
	    ['cholesterol' = {
	          'type' : 'fasting', 'units' : 'mg/dl', 'total_chol' : 320, 'hdl' : 100, 'ldl' : 240  
	        }
	    ]
	}
}