from OHA.Defaults import Defaults
from OHA.__unit import convert_height_unit
from OHA.__utilities import calculate_waist_hip_ratio, calculate_bmi

targets = {
    'general': {
        'active_time': 150,
        'activity_type': 'moderate',
        'fruit': 2,
        'vegetables': 5,
        'sbp': 140,
        'dbp': 90,
    },
    'diabetes': {
        'sbp': 130,
        'dbp': 80,
        'soft_drinks': 0,
        'added_sugar': 0,
        'added_salt': 0
    },
    'hypertension': {
        'sbp': 120,
        'dbp': 80,
        'added_salt': 0,
    }
}


def has_condition(c, conditions):
    for condition in conditions:
        if condition == c:
            return True

    return False


def assess_waist_hip_ratio(waist, hip, gender):
    _assessment_code = ""
    _target = ""

    whr = calculate_waist_hip_ratio(
        convert_height_unit(
            waist[0],
            waist[1] or Defaults.waist_unit,
            Defaults.waist_unit
        ),
        convert_height_unit(hip[0],  hip[1] or Defaults.hip_unit, Defaults.hip_unit)
    )
    if gender == "F":
        _target = 0.85
        if whr >= 0.85:
            _assessment_code = "WHR-H"
        else:
            _assessment_code = "WHR-N"
    if gender == "M":
        _target = 0.9
        if whr >= 0.9:
            _assessment_code = "WHR-H"
        else:
            _assessment_code = "WHR-N"

    whr_output = {
        'value': whr,
        'assessment_code': _assessment_code,
        'target': _target
    }

    return whr_output


def assess_smoking_status(smoking):
    _target = 0

    if smoking['current'] == 1:
        _value = 1
        _assessment_code = "SM-R"
    elif (smoking['ex_smoker']) & (smoking['quit_within_year']):
        _value = 1
        _assessment_code = "SM-A-1"
    elif smoking['ex_smoker']:
        _value = 0
        _assessment_code = "SM-A-2"
    else:
        _value = 0
        _assessment_code = "SM-G"

    smoking_output = {
        'value': _value,
        'assessment_code': _assessment_code,
        'target': _target
    }

    return smoking_output


def assess_blood_pressure(bp, conditions):
    _assessment = ""
    _assessment_code = ""
    _target = ""

    _sbp = bp['sbp'][0]
    _dbp = bp['dbp'][0]

    if _sbp > 160:
        _assessment = "HIGH RISK"
        _assessment_code = "BP-HR-0"

    elif has_condition('diabetes', conditions):
        if _sbp > 130:
            _assessment = "OFF TARGET"
            _assessment_code = "BP-DM-0"
            _target = 130
        else:
            _assessment = "ON TARGET"
            _assessment_code = "BP-DM-1"
            _target = 130
    elif (_sbp < 140) and (_sbp >= 120):
        _assessment = "OFF TARGET, MILD"
        _assessment_code = "BP-NoHx-0"
        _target = 120
    elif _sbp > 140:
        _assessment = "OFF TARGET, ELEVATED"
        _assessment_code = "BP-NoHx-1"
        _target = 120

    bp_output = {
        'bp': str(_sbp) + "/" + str(_dbp),
        'assessment_code': _assessment_code,
        'assessment': _assessment,
        'target': _target
    }
    return bp_output


def assess_bmi(bmi):
    _target = "18.5 - 24.9"

    if bmi < 18.5:
        _assessment_code = "UW"
    elif bmi < 25:
        _assessment_code = "NW"
    elif bmi < 30:
        _assessment_code = "OW"
    else:
        _assessment_code = "OB"

    bmi_output = {
        'value': bmi,
        'assessment_code': _assessment_code,
        'target': _target
    }

    return bmi_output


def assess_diet(diet_history, conditions):
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

    if diet_history['fruit'] < targets['general']['fruit'] \
            and diet_history['veg'] < targets['general']['vegetables']:
        _assessment = "BOTH OFF TARGET"
        _assessment_code = 0
        _target_message = ""
    elif ((diet_history['fruit'] < targets['general']['fruit'])
          and (diet_history['veg'] >= targets['general']['vegetables'])):
        _assessment = "PARTIAL OFF TARGET"
        _assessment_code = 1
        _target_message = "Two serves of fruit and 5 serves of vegetables"
    elif ((diet_history['fruit'] > targets['general']['fruit'])
          and (diet_history['veg'] < targets['general']['vegetables'])):
        _assessment = "PARTIAL OFF TARGET"
        _assessment_code = 2
        _target_message = "Two serves of fruit and 5 serves of vegetables"
    else:
        _assessment = "ON TARGET"
        _assessment_code = 3
        _target_message = "Two serves of fruit and 5 serves of vegetables"

    diet_output = {
        'values': {
            'fruit': diet_history['fruit'],
            'vegetables': diet_history['veg']
        },
        'assessment_code': _assessment_code,
        'assessment': _assessment,
        'target': {
            'fruit': targets['general']['fruit'],
            'vegetables': targets['general']['vegetables']
        },
        'target_message': _target_message
    }

    return diet_output


def assess_physical_activity(active_time):
    if int(active_time) >= targets['general']['active_time']:
        _assessment_code = "PAO"
        _target = 150
        _target_message = "> 150 minutes weekly"
    else:
        _assessment_code = "PAL"
        _target = 150
    pa_output = {
        'value': active_time,
        'assessment_code': _assessment_code,
        'target': _target,
    }

    return pa_output
