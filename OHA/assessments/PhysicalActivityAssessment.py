from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class PhysicalActivityAssessment(Assessment):
    def __init__(self, input_data=None):
        super(PhysicalActivityAssessment, self).__init__(input_data)

    @property
    def __active_time(self):
        return self._get_data()['active_time']

    @property
    def __targets_active_time(self):
        return self._get_data()['targets_active_time']

    def assess(self):
        target = '150 minutes'

        if int(self.__active_time) >= self.__targets_active_time:
            result_code = 'PA-1'
        else:
            result_code = 'PA-2'

        return dict(value=self.__active_time, code=result_code, target=target)
