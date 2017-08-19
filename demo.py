from OpenHealthAlgorithms.Diabetes import Diabetes
from OpenHealthAlgorithms.Framingham import Framingham
from OpenHealthAlgorithms.WHO import WHO

params = {
    'gender': 'M',
    'age': 40,
    'systolic': 150,
    'diastolic': 92,
    'weight': 92,
    'height': 1.5,
    'waist': 50,
    'hip': 90,
}
result = Diabetes().calculate(params)
print('--> Diabetes:', result)

params = {
    'gender': 'F',
    'age': 40,
    'total_cholesterol': 170,
    'hdl_cholesterol': 45,
    'systolic': 125,
    'on_bp_medication': False,
    'is_smoker': False,
    'has_diabetes': False,
}
result = Framingham().calculate(params)
print('--> Framingham:', result)

params = {
    'gender': "M",
    'age': 30,
    'systolic_blood_pressure_1': 130,
    'systolic_blood_pressure_2': 145,
    'cholesterol': 5,
    'is_smoker': True,
    'has_diabetes': True,
    'region': 'SEARD'
}

result = WHO().calculate(params)
print('--> WHO:', result)
