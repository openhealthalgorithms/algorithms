def format_params(params):
    return {
        key: float(value) if type(value) is int else value
        for key, value in params.items()
    }

def find_age_index(age, age_brackets):    
    for age_range in age_brackets:
        min, max = age_range.split('-')
        if ((age >= int(min)) & (age <= int(max))):
            age_index = age_range
            return age_index

