def assess_waist_hip_ratio(waist, hip, gender):
    raise NotImplementedError('Use "WHRAssessment"')


def assess_smoking_status(smoking):
    raise NotImplementedError('Use "SmokingAssessment"')


def assess_blood_pressure(bp, conditions):
    raise NotImplementedError('Use "BPAssessment"')


def assess_bmi(bmi):
    raise NotImplementedError('Use "BMIAssessment"')


def assess_diet(diet_history, conditions, targets):
    raise NotImplementedError('Use "DietAssessment"')


def assess_physical_activity(active_time, targets):
    raise NotImplementedError('Use "PhysicalActivityAssessment"')


def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):
    raise NotImplementedError('Use "DiabetesAssessment"')
