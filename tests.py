import json
import pandas as pd

#from OHA.Diabetes import Diabetes
#from OHA.Framingham import Framingham
#from OHA.HEARTS import HEARTS
#from OHA.HealthAssessment import HealthAssessment as HA
from OHA.WHO import WHO
#from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP
#from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB

def calculate_hearts_risk(row):
	# column names: country,age,gender,bp,total_chol,smoker,diabetes,cvd_risk
	is_smoker = False
	has_diabetes = False
	if row['smoker'] == '1':
		is_smoker = True

	if row['diabetes'] == '1':
		has_diabetes = True

	params = WPB().gender(row['gender']).age(row['age']).sbp1(row['bp']).sbp2(row['bp']).chol(row['total_chol'], 'mmol/l').region(row['country']).smoker(is_smoker).diabetic(has_diabetes).build()
	result = WHO().calculate(params)
	#print('--> WHO:', params, ' => ', result, '---\n')
	return result['risk_range']

print('---> running tests ---')

filename = 'OHA/tests/who_tests.csv'
tests_df = pd.read_csv(filename)
#print(tests_df.shape)
#print(tests_df.head())

tests_df['calculated'] = tests_df.apply(calculate_hearts_risk, axis=1)
tests_df['result'] = tests_df.apply(lambda x: 'equal' if x['cvd_risk'] == x['calculated'] else 'error', axis=1)

# add the date-time to the filname
filename = 'OHA/tests/who_tests_processed.csv'
print('---> completed tests ---')
tests_df.to_csv(filename)



