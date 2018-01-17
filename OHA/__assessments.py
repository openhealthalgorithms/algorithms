def assess_waist_hip_ratio(waist, hip, gender):
    raise NotImplementedError('"assess_waist_hip_ratio" method removed')


def assess_smoking_status(smoking):
    raise NotImplementedError('"assess_smoking_status" method removed')


def assess_blood_pressure(bp, conditions):
    raise NotImplementedError('"assess_blood_pressure" method removed')


def assess_bmi(bmi):
    raise NotImplementedError('"assess_bmi" method removed')


def assess_diet(diet_history, conditions, targets):
    """
    General Rules:
    - Aim for 50% fruit & vegetables (with specific targets for F&V), 25% lean protein, 25% carbohydrates
    - Minimise amount of fast foods, processed foods
    - Replace soda with non-sugary alternatives
    - Limit amount of added salt & sugar - for diabetics and hypertensives, target is 0
    - If trying to lose weight, avoid hotel or fast food (not sure what is in them)
    - For diabetes:
        - no added sugar
        - If BMI > 25, aim for weight loss of 600-700 calories per day
    - For Hypertensive:
        - no added salt
    Step 1: Assess general diet, fruits & vegetables based on targets (2 fruits & 5 vegetables per day)
    Step 2: Proportion of carbohydrates - should be 25% (other 25% lean protein, 50% vegetables, salads)
    Step 3: Amount of soda or other added sugars
    """

    if diet_history['fruit'] < targets['general']['diet']['fruit'] \
            and diet_history['veg'] < targets['general']['diet']['vegetables']:
        # Both F&V off target
        result_code = 'NUT-3'
    elif ((diet_history['fruit'] < targets['general']['diet']['fruit'])
          and (diet_history['veg'] >= targets['general']['diet']['vegetables'])):
        # Partial F&V off target
        result_code = 'NUT-2'
    elif ((diet_history['fruit'] > targets['general']['diet']['fruit'])
          and (diet_history['veg'] < targets['general']['diet']['vegetables'])):
        # Partial F&V off target
        result_code = 'NUT-2'
    else:
        # Partial F&V ON target
        result_code = 'NUT-1'

    diet_output = {
        'values': {
            'fruit': diet_history['fruit'],
            'vegetables': diet_history['veg']
        },
        'code': result_code
    }

    return diet_output


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
