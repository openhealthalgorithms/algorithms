<<<<<<< HEAD
from OHA.__sg_helpers import age_modifier_fre_points, calculate_smoking_points, calculate_cholesterol_points, calculate_bp_points, calculate_fre_score
from OHA.Framingham import Framingham
from OHA.SgFramingham import SgFramingham
from OHA.HEARTS import HEARTS
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB
from OHA.param_builders.sg_framingham_param_builder import SGFraminghamParamsBuilder as SGFPB

'''
=======
from OHA.SgFramingham import SgFramingham
from OHA.param_builders.sg_framingham_param_builder import SGFraminghamParamsBuilder as SGFPB

"""
>>>>>>> f0d0ede6d8135bcb9040ba1038e59fb1db70f85d
ethnicities = ['malay', 'chinese', 'indian']
ethnicity = 'malay'
gender = 'female'
age = 36
t_chol = 4.6
chol_units = 'mmol/l'
hdl = 1.8
sbp = 160
sbp_rx = False
is_smoker = True
has_diabetes = False
<<<<<<< HEAD
'''

params = SGFPB().gender('male').age(60).ethnicity('indian').t_chol(4.6, 'mmol/L').hdl_chol(1.8, 'mmol/L').sbp(125).smoker(True).diabetic(True).bp_medication(False).build()
=======
"""

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

>>>>>>> f0d0ede6d8135bcb9040ba1038e59fb1db70f85d
print(params)
result = SgFramingham().calculate(params)
print('--> Sg Framingham:', result)
print()

"""
if ethnicity in ethnicities:

    if is_smoker == True:
        smoking_points = calculate_smoking_points(age, gender)
    else:
        smoking_points = 0
<<<<<<< HEAD
    
=======

>>>>>>> f0d0ede6d8135bcb9040ba1038e59fb1db70f85d
    cholesterol_points = calculate_cholesterol_points(age, gender, t_chol, hdl)

    sbp_points = calculate_bp_points(gender, sbp, sbp_rx)

    fre_points = int(age_points) + int(smoking_points) + int(cholesterol_points) + int(sbp_points)

    fre_score = calculate_fre_score(gender, ethnicity, fre_points)

    print('\n ---- points = %s ' % fre_points)
    print('\n ---- 10 year risk score is %s ' % fre_score)

elif ethnicity == 'caucasian':
    # use the standard FRE
    if gender == "female":
        gender = "F"
    else:
        gender = "M"
<<<<<<< HEAD
        
=======

>>>>>>> f0d0ede6d8135bcb9040ba1038e59fb1db70f85d
    params = FPB().gender(gender).age(age).t_chol(t_chol, chol_units).hdl_chol(hdl, chol_units) \
              .sbp(sbp).smoker(is_smoker).diabetic(has_diabetes).bp_medication(sbp_rx).build()
    result = Framingham().calculate(params)
    print('--> Framingham:', result)
    print()

else:
    # use the standard WHO/ISH
    # define which to use here
    print("Not Calculated")
"""
<<<<<<< HEAD

=======
>>>>>>> f0d0ede6d8135bcb9040ba1038e59fb1db70f85d
