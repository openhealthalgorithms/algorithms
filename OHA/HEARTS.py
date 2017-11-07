import json

from OHA.Diabetes import Diabetes
from OHA.__assessments import assess_waist_hip_ratio, assess_smoking_status, assess_blood_pressure, assess_bmi, \
    has_condition, assess_diet, assess_physical_activity
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class HEARTS(object):
    """

    """

    @staticmethod
    def estimate_cvd_risk(age, high_risk_condition):
        # If age > assessment_age and NO high risk conditions
        assessment_age = 40

        if age < assessment_age:
            return False, "Not for CVD Risk as Age < 40"
        elif high_risk_condition[0]:
            return False, "Has High Risk Condition"
        else:
            return True, "Continue"

    @staticmethod
    def calculate_diabetes_status(conditions, bsl_type, bsl_units, bsl_value):

        # "assessment": "blood pressure off target",
        # assessment_message
        # "assessment_code" : ""
        # "bp": "145/91",
        # "target": 130,
        # "target_message": "target set for patient with diabetes"

        _assessment = ""
        _assessment_code = ""
        _assessment_message = ""
        _target = ""
        _target_message = ""

        diabetes_data = {}
        # move to a helper function
        if bsl_units == 'mg/dl':
            bsl_value = round(float(bsl_value) / 18, 1)

        for condition in conditions:
            if condition == "diabetes":
                # return True
                _assessment = True
                _assessment_message = "History of Diabetes"
                _assessment_code = 'BSL-R'
                _target = '',
                _target_message = ''
            else:
                if bsl_type == "random":
                    if bsl_value >= 11.1:
                        _assessment = True
                        _assessment_message = "Looks like newly diagnosed diabetes"
                        _assessment_code = 'DM-NEW'
                        _target = ''
                        _target_message = ''
                        # diabetes_data['dx'] = True
                        # diabetes_data['diagnosis_type'] = 'DM-New'
                        # diabetes_data['code'] = 'BSL-R'
                        # return (diabetes_data, "Looks like newly diagnosed diabetes")
                    elif bsl_value > 7:
                        _assessment = False
                        _assessment_message = "You are at risk of developing Diabetes"
                        _assessment_code = 'DM-PRE'
                        _target = ''
                        _target_message = ''
                        # diabetes_data['dx'] = False
                        # diabetes_data['diagnosis_type'] = 'DM-Pre'
                        # diabetes_data['code'] = 'BSL-A'
                        # return (diabetes_data, "You are at risk of developing diabetes")
                    else:
                        _assessment = False
                        _assessment_message = "Normal Blood Sugar. No Diabetes"
                        _assessment_code = 'DM-NONE'
                        _target = ''
                        _target_message = ''
                        # diabetes_data['dx'] = False
                        # diabetes_data['diagnosis_type'] = 'DM-NA'
                        # diabetes_data['code'] = 'BSL-G'
                        # return (diabetes_data, "BSL-G", "Blood sugar normal")
            # return False
            diabetes_output = {
                'value': bsl_value,
                'assessment': _assessment,
                'assessment_code': _assessment_code,
                'assessment_message': _assessment_message,
                'target': _target,
                'target_message': _target_message
            }

            return diabetes_output

    @staticmethod
    def load_messages():
        file = 'guideline_content.json'
        with open(file) as json_data:
            data = json.load(json_data)

        return data["body"]["messages"]

    @staticmethod
    def load_guidelines(guideline_key):
        file = 'guideline_hearts.json'
        with open(file) as json_data:
            data = json.load(json_data)

        return data

    @staticmethod
    def high_risk_condition_check(age, blood_pressure, conditions):

        _assessment = ""
        _assessment_code = ""
        _target = ""
        _target_message = ""

        # Known heart disease, stroke, transient ischemic attack, DM, kidney disease (for assessment, if this has not been done)
        high_risk_conditions = ['CVD', 'CAD', 'AMI', 'HEART ATTACK', 'CVA', 'TIA', 'STROKE', 'CKD', 'PVD']
        # Return whether medical history contains any of these

        for condition in conditions:
            print(condition)
            if condition.upper() in high_risk_conditions:
                # _assessment = True
                # _assessment_message = 'Has High Risk Condition %s' % condition.upper()
                # _assessment_code = ""
                return (True, 'Has High Risk Condition %s' % condition.upper())

        # check for other high risk states such as BP > 160 and age > 60 + diabetes (including newly suggested)
        # if (assessment[])
        # blood pressure [value, observation_type]
        sbp = blood_pressure['sbp'][0]
        dbp = blood_pressure['dbp'][0]

        if ((sbp > 200) or (dbp > 120)):
            # _assessment = True
            # _assessment_code = "HRC-HTN"
            return (True, "HRC-HTN", 'Severely high blood pressure. Seek emergency care immediately')
        elif ((age < 40) and ((sbp >= 140) or (dbp >= 90))):
            # _assessment = True
            # _assessment_code = "HRC-AGE-BP"
            return (
                True, "HRC-AGE-BP",
                'High blood pressure in under 40, should be investigated for secondary hypertension')
        else:
            # _assessment = False
            # _assessment = "No High Risk Condition"
            return False, "No High Risk Condition"

    @staticmethod
    def calc_cvd_risk(inputParams):
        """
        Call the relevant WHO model and compute
        """

        # cvd_risk = (20, '10-20')
        cvd_risk = (30, '20-30')
        return cvd_risk

    @staticmethod
    def calculate():
        assessment = {}

        # load guidelines
        guidelines = HEARTS.load_guidelines('hearts')["body"]

        # load message
        messages = HEARTS.load_messages()

        # load in the response object
        with open('request.json') as json_data:
            data = json.load(json_data)

        # unpack the request, validate it and set up the params
        demographics = data['body']['demographics']
        measurements = data['body']['measurements']
        smoking = data['body']['smoking']
        physical_activity = data['body']['physical_activity']
        diet_history = data['body']['diet_history']
        medical_history = data['body']['medical_history']
        pathology = data['body']['pathology']
        medications = []

        print('--- Running lifestyle and risk factor assessment ---')
        bmi = assess_bmi(measurements['weight'], measurements['height'])
        whr = assess_waist_hip_ratio(measurements['waist'], measurements['hip'], demographics['gender'])
        smoker = assess_smoking_status(smoking)

        # assess diabetes status or risk
        print('--- Check diabetes status---')
        diabetes_status = HEARTS.calculate_diabetes_status(
            medical_history, pathology['bsl']['type'], pathology['bsl']['units'], pathology['bsl']['value']
        )

        print(diabetes_status)
        # If does not have diabetes
        if diabetes_status['assessment_code'] == 'DM-NONE':
            # calculate diabetes risk score
            diabetes_params = DiabetesParamsBuilder() \
                .gender(demographics['gender']) \
                .age(demographics['age']) \
                .waist(measurements['waist']) \
                .hip(measurements['hip']) \
                .height(measurements['height']) \
                .weight(measurements['weight']) \
                .sbp(measurements['sbp']) \
                .dbp(measurements['dbp']) \
                .build()
            diabetes_risk = Diabetes().calculate(diabetes_params)['risk']
        else:
            # newly diagnosed diabetes, add to existing conditions list
            conditions = medical_history['conditions']
            conditions.append('diabetes')
            medical_history['conditions'] = conditions
            diabetes_risk = "NA"
            # print('diabetes status is %s ' % assessment['diabetes_status'][1])

        diabetes_status['risk'] = diabetes_risk
        assessment['diabetes'] = diabetes_status
        '''assessment['diabetes'] = {
                        'risk' : diabetes_risk,
                        'status' : diabetes_status
                    }
                '''
        print('--- High Risk Condition Check ---')
        blood_pressure = {
            'sbp': measurements['sbp'],
            'dbp': measurements['dbp']
        }
        print(blood_pressure)

        bp_assessment = assess_blood_pressure(blood_pressure, medical_history['conditions'], medications)
        assessment['blood_pressure'] = bp_assessment
        '''
        assessment['blood_pressure'] = {
            'bp' : str(measurements['sbp'][0]) + "/" + str(measurements['dbp'][0]),
            'assessment_code' : bp_assessment[0], 
            'assessment' : bp_assessment[1],
            'target' : bp_assessment[2],
            'target_message' : bp_assessment[3]
        }
        '''

        diet = assess_diet(diet_history, medical_history['conditions'])

        exercise = assess_physical_activity(physical_activity)

        assessment['lifestyle'] = {
            'bmi': bmi,
            'whr': whr,
            'diet': diet,
            'exercise': exercise,
            'smoking': smoker
        }

        age = demographics['age']
        # work out how to add in diabetes if newly diagnosed?
        print(medical_history['conditions'])
        high_risk_condition = HEARTS.high_risk_condition_check(demographics['age'], blood_pressure,
                                                               medical_history['conditions'])
        print(high_risk_condition)

        assessment['cvd_assessment'] = {
            'high_risk_condition': high_risk_condition
        }

        # Determine whether eligible for CVD risk assessment
        estimate_cvd_risk_calc = HEARTS.estimate_cvd_risk(age, high_risk_condition)
        # print('high risk output %s ' % assessment['high_risk'][0])
        # if not high_risk_condition[0]:
        if estimate_cvd_risk_calc[0]:
            # if not already at high risk then calculate CVD risk
            print('do cvd check')
            # use the WHO model to do the cvd risk assessment
            cvd_risk = HEARTS.calc_cvd_risk(assessment)
            # use the key to look up the guidelines output
            assessment['cvd_assessment']['cvd_risk_result'] = cvd_risk
            print(cvd_risk)
            assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk'][cvd_risk[1]]
            # print(guidelines['cvd_risk'][assessment['cvd_risk'][1]])
        else:
            cvd_calc = estimate_cvd_risk_calc[1]
            print(cvd_calc)
            # assessment['cvd_assessment']['guidelines'] = guidelines['cvd_risk']['Refer']

        # finally formualate guidelines
        print("--- Writing Your Results ----")
        with open('response.json', 'w') as fp:
            json.dump(assessment, fp)


if __name__ == "__main__":
    print('---Starting Hearts Assessment----')
    HEARTS().calculate()
