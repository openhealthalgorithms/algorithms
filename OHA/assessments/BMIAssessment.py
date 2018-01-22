from OHA.Defaults import Defaults
from OHA.__unit import convert_height_unit, convert_weight_unit
from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class BMIAssessment(Assessment):
    def __init__(self, input_data=None):
        super(BMIAssessment, self).__init__(input_data)

    @property
    def __weight(self):
        weight = self._get_data()['weight']
        return convert_height_unit(weight[0], weight[1] or Defaults.weight_unit, Defaults.weight_unit)

    @property
    def __height(self):
        height = self._get_data()['height']
        return convert_weight_unit(height[0], height[1] or Defaults.height_unit, Defaults.height_unit)

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
