def format_params(params):
    return {
        key: float(value) if type(value) is int else value
        for key, value in params.items()
    }

def convert_cholesterol_unit(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    elif to_unit.lower() == 'mmol/l':
        return (value * 0.02586)
    elif to_unit.lower() == 'mg/dl':
        return value * 88.57
    else:
        return None

