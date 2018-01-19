from OHA.__sg_helpers import age_modifier_fre_points, calculate_smoking_points, calculate_cholesterol_points, calculate_bp_points, calculate_fre_score

ethnicity = 'indian'
age = 43
t_chol = 4.6
hdl = 1.8
sbp = 160
sbp_rx = False
is_smoker = True
age_points = age_modifier_fre_points(age, gender)

if is_smoker == True:
    smoking_points = calculate_smoking_points(gender, age)
else:
    smoking_points = 0
 
cholesterol_points = calculate_cholesterol_points(gender, age, t_chol, hdl)

sbp_points = calculate_bp_points(gender, sbp, sbp_rx)

fre_points = int(age_points) + int(smoking_points) + int(cholesterol_points) + int(sbp_points)

fre_score = calculate_fre_score(gender, ethnicity, fre_points)


print('\n ---- points = %s ' % fre_points)
print('\n ---- 10 year risk score is %s ' % fre_score)