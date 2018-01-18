from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class HighRiskConditionAssessment(Assessment):
    def __init__(self, input_data=None):
        super(HighRiskConditionAssessment, self).__init__(input_data)

    @property
    def __age(self):
        return self._get_data()['age']

    @property
    def __bp(self):
        return self._get_data()['bp']

    @property
    def __conditions(self):
        return self._get_data()['conditions']

    @property
    def __hrc(self):
        return self._get_data()['hrc']

    def assess(self):
        has_high_risk_condition = False
        result_code = ''

        hrc_value = None
        for condition in self.__conditions:
            if condition.upper() in self.__hrc:
                has_high_risk_condition = True
                result_code = 'HR-0'
                hrc_value = condition
            else:
                hrc_value = None

        if not has_high_risk_condition:
            sbp = self.__bp['sbp'][0]
            dbp = self.__bp['dbp'][0]

            if sbp > 200 or dbp > 120:
                has_high_risk_condition = True
                result_code = 'HR-1'
            elif self.__age < 40 and (sbp >= 140 or dbp >= 90):
                result_code = 'HR-2'

        return dict(status=has_high_risk_condition, reason=hrc_value, code=result_code)
