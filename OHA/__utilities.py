def calculate_bmi(weight, height):
    body_mass_index = round(float(weight / (height * height)), 2)
    return body_mass_index


def calculate_waist_hip_ratio(waist, hip):
    waist_hip_ratio = round(float(waist / hip), 2)
    return waist_hip_ratio


def cvd_risk_string(cvd_risk):
    if cvd_risk == 10:
        return '<10'
    elif cvd_risk == 20:
        return '10-20'
    elif cvd_risk == 30:
        return '20-30'
    elif cvd_risk == 40:
        return '30-40'
    elif cvd_risk == 50:
        return '>40'
    else:
        return '>40'
