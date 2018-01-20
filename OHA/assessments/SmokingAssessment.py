from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class SmokingAssessment(Assessment):
    def __init__(self, input_data=None):
        super(SmokingAssessment, self).__init__(input_data)

    @property
    def __smoking(self):
        return self._get_data()['smoking']

    @property
    def __current_smoker(self):
        return self.__smoking['current']

    @property
    def __ex_smoker(self):
        return self.__smoking['ex_smoker']

    @property
    def __quit_within_year(self):
        return self.__smoking['quit_within_year']

    def assess(self):
        is_smoker = self.__current_smoker == 1
        smoking_calc = False

        if self.__current_smoker == 1:
            smoking_calc = True
            result_code = 'SM-1'
        elif self.__ex_smoker and self.__quit_within_year:
            smoking_calc = True
            result_code = 'SM-2'
        elif self.__ex_smoker:
            result_code = 'SM-3'
        else:
            result_code = 'SM-4'

        return dict(code=result_code, status=is_smoker, smoking_calc=smoking_calc)
