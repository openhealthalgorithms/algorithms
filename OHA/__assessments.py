from OHA.Defaults import Defaults
from OHA.__unit import convert_height_unit
from OHA.__utilities import calculate_waist_hip_ratio


def has_condition(c, conditions):
    for condition in conditions:
        if condition == c:
            return True

    return False


def assess_waist_hip_ratio(waist, hip, gender):
    raise NotImplementedError('"assess_waist_hip_ratio" method removed')


def assess_smoking_status(smoking):
    is_smoker = False
    smoking_calc = False

    if smoking['current'] == 1:
        is_smoker = True
        smoking_calc = True
        result_code = 'SM-1'
    elif (smoking['ex_smoker']) & (smoking['quit_within_year']):
        # quit within 1 year, considered smoker for calc
        is_smoker = False
        smoking_calc = True
        result_code = 'SM-2'
    elif smoking['ex_smoker']:
        is_smoker = False
        result_code = 'SM-3'
    else:
        is_smoker = False
        result_code = 'SM-4'

    smoking_status = {
        'code': result_code,
        'status': is_smoker,
        'smoking_calc': smoking_calc,
    }

    return smoking_status


def assess_blood_pressure(bp, conditions):
    result_code = ""

    _sbp = bp['sbp'][0]
    _dbp = bp['dbp'][0]

    if _sbp > 160:
        result_code = "BP-2"

    elif has_condition('diabetes', conditions):
        if _sbp > 130:
            result_code = "BP-3B"
            target = "130/80"
        else:
            result_code = "BP-3A"
    elif (_sbp <= 140) and (_sbp >= 120):
        result_code = "BP-1A"
        target = "140/90"
    elif _sbp > 140:
        result_code = "BP-1B"
        target = "140/90"
    elif _sbp <= 120:
        result_code = "BP-0"
        target = "140/90"

    bp_output = {
        'bp': str(_sbp) + "/" + str(_dbp),
        'code': result_code,
        'target': target
    }
    return bp_output


def assess_bmi(bmi):
    target = "18.5 - 24.9"

    if bmi < 18.5:
        result_code = "BMI-1"
    elif bmi < 25:
        result_code = "BMI-0"
    elif bmi < 30:
        result_code = "BMI-2"
    else:
        result_code = "BMI-3"

    bmi_output = {
        'value': bmi,
        'code': result_code,
        'target': target
    }

    return bmi_output


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
        result_code = "NUT-3"
    elif ((diet_history['fruit'] < targets['general']['diet']['fruit'])
          and (diet_history['veg'] >= targets['general']['diet']['vegetables'])):
        # Partial F&V off target
        result_code = "NUT-2"
    elif ((diet_history['fruit'] > targets['general']['diet']['fruit'])
          and (diet_history['veg'] < targets['general']['diet']['vegetables'])):
        # Partial F&V off target
        result_code = "NUT-2"
    else:
        # Partial F&V ON target
        result_code = "NUT-1"

    diet_output = {
        'values': {
            'fruit': diet_history['fruit'],
            'vegetables': diet_history['veg']
        },
        'code': result_code
    }

    return diet_output


def assess_physical_activity(active_time, targets):
    target = "150 minutes"
    if int(active_time) >= targets['general']["physical_activity"]['active_time']:
        # targets being met
        result_code = "PA-1"
    else:
        # targets not being met
        result_code = "PA-2"
    pa_output = {
        'value': active_time,
        'code': result_code,
        'target': target
    }

    return pa_output


def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):
    status = False
    code = ""

    # move to a helper function
    if bsl_units == 'mg/dl':
        bsl_value = round(float(bsl_value) / 18, 1)

    for condition in conditions:
        if condition == "diabetes":
            status = True
            code = 'DM-4'
        else:
            if bsl_type == "random":
                # for random BSL, BSL > 11.1 with symptoms is diagnostic
                if bsl_value >= 11.1:
                    status = True
                    # Possible new diagnosis
                    code = 'DM-3'
            elif bsl_type == "fasting":
                # if fasting, then BSL > 7 is diagnostic
                if bsl_value > 7:
                    status = True
                    code = 'DM-3'
                elif bsl_value > 6.1:
                    # if fasting, bsl 6.1-7 "prediabetes"
                    status = True
                    code = 'DM-2'
            elif bsl_type == "hba1c":
                # if >= 6.5%, diagnostic
                if bsl_value >= 6.5:
                    status = True

        # return False
        diabetes_output = {
            'value': bsl_value,
            'status': status,
            'code': code
        }

        return diabetes_output


def check_medications(search, medications):
    for medication in medications:
        if str.upper(medication) == str.upper(search):
            return True
        else:
            return False
