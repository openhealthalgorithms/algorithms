from OHA.Diabetes import Diabetes
from OHA.Framingham import Framingham
from OHA.WHO import WHO

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

params = {
    'gender': 'F',
    'age': 40,
    'total_cholesterol': 170,
    'total_cholesterol_unit': 'mg/dl',
    'hdl_cholesterol': 45,
    'hdl_cholesterol_unit': 'mg/dl',
    'systolic': 125,
    'on_bp_medication': False,
    'is_smoker': False,
    'has_diabetes': False,
}
result = Framingham().calculate(params)
print('--> Framingham:', result)

params = {
    'gender': "M",
    'age': 50,
    'systolic_blood_pressure_1': 150,
    'systolic_blood_pressure_2': 170,
    'cholesterol': 7,
    'cholesterol_unit': 'mmol/l',
    'is_smoker': True,
    'has_diabetes': True,
    'region': 'SEARD'
}

result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)


params = {
    'gender': "M",
    'age': 50,
    'systolic_blood_pressure_1': 150,
    'systolic_blood_pressure_2': 170,
    'cholesterol': 7,
    'cholesterol_unit': 'mmol/l',
    'is_smoker': True,
    'has_diabetes': True,
    'region': 'AFRD'
}

result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)


params = {
    'gender': "M",
    'age': 50,
    'systolic_blood_pressure_1': 150,
    'systolic_blood_pressure_2': 170,
    'cholesterol': 7,
    'cholesterol_unit': 'mmol/l',
    'is_smoker': True,
    'has_diabetes': True,
    'region': 'AFRE'
}

result = WHO().calculate(params)
print('--> WHO:', params['region'], ' => ',  result)
