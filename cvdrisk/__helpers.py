def format_params(params):
    return {
        key: float(value) if type(value) is int else value
        for key, value in params.items()
    }


def convert_cholesterol_unit(value, from_unit, to_unit):
    if from_unit.lower() == to_unit.lower():
        return value
    elif to_unit.lower() == 'mmol/l':
        return value * 0.02586
    elif to_unit.lower() == 'mg/dl':
        return value * 88.57
    else:
        return None


def convert_weight_unit(value, from_unit, to_unit):
    if from_unit.lower() == to_unit.lower():
        return value
    elif to_unit.lower() == 'lb':
        return value / 0.45359237
    elif to_unit.lower() == 'kg':
        return value * 0.45359237
    else:
        return None

def calculate_bmi(height, weight):
    #process this and ensure the correct values etc
    return round(weight/(height*height), 1)

def calculate_waist_hip_ratio(waist, hip):
    return round((waist/hip), 1)

def convert_height_unit(value, from_unit, to_unit):
    if from_unit.lower() == to_unit.lower():
        return value
    elif to_unit.lower() == 'm' and from_unit.lower() == 'ft':
        return value * 3.28084
    elif to_unit.lower() == 'm' and from_unit.lower() == 'in':
        return value * 39.3701
    elif to_unit.lower() == 'cm' and from_unit.lower() == 'ft':
        return value * 0.0328084
    elif to_unit.lower() == 'cm' and from_unit.lower() == 'in':
        return value * 0.393701
    elif to_unit.lower() == 'ft' and from_unit.lower() == 'm':
        return value * 0.3048
    elif to_unit.lower() == 'ft' and from_unit.lower() == 'cm':
        return value * 30.48
    elif to_unit.lower() == 'in' and from_unit.lower() == 'm':
        return value * 0.0254
    elif to_unit.lower() == 'in' and from_unit.lower() == 'cm':
        return value * 2.54
    else:
        return None