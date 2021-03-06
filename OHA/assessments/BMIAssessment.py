from OHA.assessments.BaseAssessment import BaseAssessment
from OHA.helpers.converters.HeightConverter import HeightConverter
from OHA.helpers.converters.WeightConverter import WeightConverter

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class BMIAssessment(BaseAssessment):
    def __init__(self, input_data=None):
        super(BMIAssessment, self).__init__(input_data)

    @property
    def __weight(self):
        weight = self._get_data()['weight']
        return WeightConverter(weight[0]).from_unit(weight[1]).converted

    @property
    def __height(self):
        height = self._get_data()['height']
        return HeightConverter(height[0]).from_unit(height[1]).converted

    @property
    def __bmi(self):
        return round(float(self.__weight / (self.__height * self.__height)), 2)

    def assess(self):
        target = '18.5 - 24.9'

        bmi = self.__bmi
        if bmi < 18.5:
            result_code = 'BMI-1'
        elif bmi < 25:
            result_code = 'BMI-0'
        elif bmi < 30:
            result_code = 'BMI-2'
        else:
            result_code = 'BMI-3'

        bmi_output = dict(value=bmi, code=result_code, target=target)

        return bmi_output
