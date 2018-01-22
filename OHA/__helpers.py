def format_params(params):
    raise NotImplementedError('Use "ParamFormatter"')


def find_age_index(age, age_brackets):    
    for age_range in age_brackets:
        _min, _max = age_range.split('-')
        if int(_min) <= age <= int(_max):
            age_index = age_range
            return age_index
