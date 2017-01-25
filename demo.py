from OpenHealthAlgorithms.Diabetes import Diabetes

params = {
    'gender':    'M',
    'age':       40,
    'systolic':  150,
    'diastolic': 92,
    'weight':    92,
    'height':    1.5,
    'waist':     50,
    'hip':       90,
}
result = Diabetes().calculate(params)
print(result)
