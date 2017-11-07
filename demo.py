from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.HEARTS import HEARTS
from OHA.WHO import WHO
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP

params = DBP()\
    .gender("M").age(40).sbp(150).dbp(92).weight(92, 'kg').height(1.5, 'm').waist(50, 'cm').hip(90, 'cm').build()
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


result = HEARTS().calculate()
print('--> HEARTS: => ',  result)
