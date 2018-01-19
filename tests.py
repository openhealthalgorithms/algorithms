import json
import pandas as pd

from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.HEARTS import HEARTS
from OHA.HealthAssessment import HealthAssessment as HA
from OHA.WHO import WHO
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB

filename = 'OHA/tests/who_tests.csv'
tests = pd.read_csv(filename)
print(tests.shape)
print(tests.head())

print('\n --- Running Tests ---')
params = WPB().gender("M").age(43).sbp1(150).sbp2(140).chol(4.1, 'mmol/l').region('AFRE').smoker().diabetic(True).build()
result = WHO().calculate(params)
print('--> WHO:', params, ' => ', result)

params = WPB().gender("M").age(43).sbp1(180).sbp2(180).chol(5.1, 'mmol/l').region('AFRD').smoker().diabetic(True).build()
result = WHO().calculate(params)
print('--> WHO:', params, ' => ', result)

params = WPB().gender("F").age(52).sbp1(165).sbp2(166).chol(6.1, 'mmol/l').region('AFRD').smoker(True).diabetic(False).build()
result = WHO().calculate(params)
print('--> WHO:', params, ' => ', result)

print('\n --- Running Tests ---')
params = WPB().gender("M").age(43).sbp1(150).sbp2(140).chol(4.1, 'mmol/l').region('AFRD').smoker().diabetic(True).build()
result = WHO().calculate(params)
print('--> WHO:', params, ' => ', result)

print('\n --- Running Tests ---')
params = WPB().gender("F").age(40).sbp1(169).sbp2(169).chol(5.2, 'mmol/l').region('AFRD').smoker(True).diabetic(False).build()
result = WHO().calculate(params)
print('--> WHO:', params, ' => ', result)
