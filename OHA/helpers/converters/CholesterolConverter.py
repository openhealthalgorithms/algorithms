from OHA.Defaults import Defaults
from OHA.helpers.converters.BaseConverter import BaseConverter

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class CholesterolConverter(BaseConverter):
    def __init__(self, _value, _from=None, _to=None):
        super(CholesterolConverter, self).__init__(_value, _from, _to)

    def _from_values(self):
        return ['mmol/l', 'mg/dl']

    def _to_values(self):
        return ['mmol/l', 'mg/dl']

    def _default_from_unit(self):
        return Defaults.cholesterol_unit

    def _default_to_unit(self):
        return Defaults.cholesterol_unit

    def _convert(self):
        if self._from == self._to:
            return self._value
        elif self._to == 'mmol/l':
            return self._value * 0.02586
        elif self._to == 'mg/dl':
            return self._value * 88.57
        else:
            return None
