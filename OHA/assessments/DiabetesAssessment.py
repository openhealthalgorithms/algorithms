from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class DiabetesAssessment(Assessment):
    def __init__(self, input_data=None):
        super(DiabetesAssessment, self).__init__(input_data)

    @property
    def __conditions(self):
        return self._get_data()['conditions']

    @property
    def __bsl_type(self):
        return self._get_data()['bsl_type']

    @property
    def __bsl_units(self):
        return self._get_data()['bsl_units']

    @property
    def __bsl_value(self):
        return self._get_data()['bsl_value']

    def assess(self):
        status = False
        code = ''

        bsl_value = round(float(self.__bsl_value) / 18, 1) if self.__bsl_units == 'mg/dl' else self.__bsl_value

        for condition in self.__conditions:
            if condition == 'diabetes':
                status = True
                code = 'DM-4'
            else:
                if self.__bsl_type == 'random':
                    if bsl_value >= 11.1:
                        status = True
                        code = 'DM-3'
                elif self.__bsl_type == 'fasting':
                    if bsl_value > 7:
                        status = True
                        code = 'DM-3'
                    elif bsl_value > 6.1:
                        status = True
                        code = 'DM-2'
                elif self.__bsl_type == 'hba1c':
                    if bsl_value >= 6.5:
                        status = True

        return dict(value=bsl_value, status=status, code=code)
