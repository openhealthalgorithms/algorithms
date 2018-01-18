from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class BPAssessment(Assessment):
    def __init__(self, input_data=None):
        super(BPAssessment, self).__init__(input_data)

    @property
    def __bp(self):
        return self._get_data()['bp']

    @property
    def __conditions(self):
        return self._get_data()['conditions']

    def __has_condition(self, c):
        for condition in self.__conditions:
            if condition == c:
                return True
        return False

    def assess(self):
        result_code = ''

        _sbp = self.__bp['sbp'][0]
        _dbp = self.__bp['dbp'][0]
        target = '%s/%s' % (_sbp, _dbp)

        if _sbp > 160:
            result_code = 'BP-2'

        elif self.__has_condition('diabetes'):
            if _sbp > 130:
                result_code = 'BP-3B'
                target = '130/80'
            else:
                result_code = 'BP-3A'
        elif 140 >= _sbp >= 120:
            result_code = 'BP-1A'
            target = '140/90'
        elif _sbp > 140:
            result_code = 'BP-1B'
            target = '140/90'
        elif _sbp <= 120:
            result_code = 'BP-0'
            target = '140/90'

        return dict(bp='%s/%s' % (_sbp, _dbp), code=result_code, target=target)
