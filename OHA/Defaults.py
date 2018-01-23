class Defaults(object):
    weight_unit = 'kg'
    height_unit = 'm'
    waist_unit = 'cm'
    hip_unit = 'cm'
    cholesterol_unit = 'mmol/l'
    region = 'SEARD'
    co_efficients = {
        'so10': {'F': 0.95012, 'M': 0.8893},
        'logAge': {'F': 2.32888, 'M': 3.06117},
        'logTChol': {'F': 1.20904, 'M': 1.12370},
        'logHDLChol': {'F': 0.70833, 'M': 0.93263},
        'logSBPNonRx': {'F': 2.76157, 'M': 1.93303},
        'logSBPRx': {'F': 2.82263, 'M': 1.99881},
        'logSmoking': {'F': 0.52873, 'M': 0.65451},
        'logDM': {'F': 0.69154, 'M': 0.57367},
        'calc_mean': {'F': 26.1931, 'M': 23.9802},
    }
