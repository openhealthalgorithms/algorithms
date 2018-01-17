def assess_waist_hip_ratio(waist, hip, gender):
    raise NotImplementedError('"assess_waist_hip_ratio" method removed')


def assess_smoking_status(smoking):
    raise NotImplementedError('"assess_smoking_status" method removed')


def assess_blood_pressure(bp, conditions):
    raise NotImplementedError('"assess_blood_pressure" method removed')


def assess_bmi(bmi):
    raise NotImplementedError('"assess_bmi" method removed')


def assess_diet(diet_history, conditions, targets):
    raise NotImplementedError('"assess_diet" method removed')


def assess_physical_activity(active_time, targets):
    raise NotImplementedError('"assess_physical_activity" method removed')


def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):
    raise NotImplementedError('"calculate_diabetes_status" method removed')


def check_medications(search, medications):
    for medication in medications:
        if str.upper(medication) == str.upper(search):
            return True
        else:
            return False
