from OHA.Defaults import Defaults
from OHA.__unit import convert_height_unit
from OHA.assessments.BaseAssessment import BaseAssessment
from OHA.helpers.converters.HipConverter import HipConverter
from OHA.helpers.converters.WaistConverter import WaistConverter

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class WHRAssessment(BaseAssessment):
    def __init__(self, input_data=None):
        if input_data is not None:
            if input_data['gender'] not in ['F', 'M']:
                raise ValueError('gender value must be "F" or "M"')
        super(WHRAssessment, self).__init__(input_data)

    @property
    def __waist(self):
        waist = self._get_data()['waist']
        return WaistConverter(waist[0]).from_unit(waist[1]).converted

    @property
    def __hip(self):
        hip = self._get_data()['hip']
        return HipConverter(hip[0]).from_unit(hip[1]).converted

    @property
    def __gender(self):
        return self._get_data()['gender']

    @property
    def __whr(self):
        return round(float(self.__waist / self.__hip), 2)

    def assess(self):
        result_code = 'WHR-0'
        target = 0.85 if self.__gender == 'F' else 0.9

        whr = self.__whr
        if self.__gender == 'F' and whr >= 0.85:
            result_code = 'WHR-1'
        elif self.__gender == 'M' and whr >= 0.9:
            result_code = 'WHR-2'

        return dict(value=whr, code=result_code, target=target)
