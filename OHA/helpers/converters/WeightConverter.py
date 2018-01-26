from OHA.Defaults import Defaults
from OHA.helpers.converters.BaseConverter import BaseConverter


class WeightConverter(BaseConverter):
    def __init__(self, _value, _from=None, _to=None):
        super(WeightConverter, self).__init__(_value, _from, _to)

    def _from_values(self):
        return ['lb', 'kg']

    def _to_values(self):
        return ['lb', 'kg']

    def _default_from_unit(self):
        return Defaults.weight_unit

    def _default_to_unit(self):
        return Defaults.weight_unit

    def _convert(self):
        if self._from == self._to:
            return self._value
        elif self._to == 'lb':
            return self._value / 0.45359237
        elif self._to == 'kg':
            return self._value * 0.45359237
        else:
            return None
