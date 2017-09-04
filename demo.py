from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.WHO import WHO
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB

params = {
    'gender': 'M',
    'age': 40,
    'systolic': 150,
    'diastolic': 92,
    'weight': 92,
    'weight_unit': 'kg',
    'height': 1.5,
    'height_unit': 'm',
    'waist': 50,
    'waist_unit': 'cm',
    'hip': 90,
    'hip_unit': 'cm',
}
result = Diabetes().calculate(params)
print('--> Diabetes:', result)

params = FPB().gender("F").age(40).t_chol(170, 'mg/dl').hdl_chol(45, 'mg/dl').sbp(125).build()
result = Framingham().calculate(params)
print('--> Framingham:', result)

params = WPB().gender("M").age(50).sbp1(150).sbp2(170).chol(7, 'mmol/l').region('SEARD').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)

params = WPB().gender("M").age(50).sbp1(150).sbp2(170).chol(7, 'mmol/l').region('AFRD').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)

params = WPB().gender("M").age(50).sbp1(150).sbp2(170).chol(7, 'mmol/l').region('AFRE').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)

params = WPB().gender("M").age(70).sbp1(130).sbp2(145).chol(270, 'mg/dl').smoker().diabetic().build()
result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)
