from OHA.assessments.BMIAssessment import BMIAssessment

__author__ = 'fredhersch'
__email__ = 'fred@openhealthalgorithms.org'


class SEABMIAssessment(BMIAssessment):
    """
        Calculate BMI Assessment for SEA population
    """

    def assess(self):
        target = '18.5 - 22.9'

        bmi = self.__bmi
        if bmi < 18.5:
            result_code = 'BMI-1'
        elif bmi <= 22.9:
            result_code = 'BMI-0'
        elif bmi <= 27.4:
            result_code = 'BMI-2'
        elif bmi <= 32.4:
            result_code = 'BMI-3'
        else:
            result_code = 'BMI-4'

        bmi_output = dict(value=bmi, code=result_code, target=target)

        return bmi_output
