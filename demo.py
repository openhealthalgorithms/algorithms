from OpenHealthAlgorithms.Diabetes import Diabetes
from OpenHealthAlgorithms.Framingham import Framingham

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
print '{0: <20}'.format(' --> Diabetes:'), result

params = {
   'gender':            'F',
   'age':               40,
   'total_cholesterol': 180,
   'hdl_cholesterol':   45,
   'systolic':          125,
   'on_bp_medication':  False,
   'is_smoker':         False,
   'has_diabetes':      False,
}
result = Framingham().calculate(params)
print '{0: <20}'.format(' --> Framingham:'), result
