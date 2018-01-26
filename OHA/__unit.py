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
    raise NotImplementedError('use "helpers.converter.WeightConverter"')


def convert_height_unit(value, from_unit, to_unit):
    raise NotImplementedError('use "helpers.converter.HeightConverter"')
