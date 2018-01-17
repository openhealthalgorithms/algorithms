from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class SmokingAssessment(Assessment):
    def __init__(self, input_data=None):
        super().__init__(input_data)

    def __smoking(self):
        return self._get_data()['smoking']

    def assess(self):
        is_smoker = self.__smoking()['current'] == 1
        smoking_calc = False

        if self.__smoking()['current'] == 1:
            smoking_calc = True
            result_code = 'SM-1'
        elif self.__smoking()['ex_smoker'] and self.__smoking()['quit_within_year']:
            smoking_calc = True
            result_code = 'SM-2'
        elif self.__smoking()['ex_smoker']:
            result_code = 'SM-3'
        else:
            result_code = 'SM-4'

        return dict(code=result_code, status=is_smoker, smoking_calc=smoking_calc)
