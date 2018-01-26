import abc

from OHA.helpers.converters.BaseConverter import BaseConverter


class LengthConverter(BaseConverter):
    def __init__(self, _value, _from=None, _to=None):
        super(LengthConverter, self).__init__(_value, _from, _to)

    def _from_values(self):
        return ['ft', 'in', 'm', 'cm']

    def _to_values(self):
        return ['ft', 'in', 'm', 'cm']

    @abc.abstractmethod
    def _default_from_unit(self):
        raise NotImplementedError('method not implemented')

    @abc.abstractmethod
    def _default_to_unit(self):
        raise NotImplementedError('method not implemented')

    def _convert(self):
        if self._from == self._to:
            return self._value
        elif self._to == 'm' and self._from == 'ft':
            return self._value * 3.28084
        elif self._to == 'm' and self._from == 'in':
            return self._value * 39.3701
        elif self._to == 'cm' and self._from == 'ft':
            return self._value * 0.0328084
        elif self._to == 'cm' and self._from == 'in':
            return self._value * 0.393701
        elif self._to == 'ft' and self._from == 'm':
            return self._value * 0.3048
        elif self._to == 'ft' and self._from == 'cm':
            return self._value * 30.48
        elif self._to == 'in' and self._from == 'm':
            return self._value * 0.0254
        elif self._to == 'in' and self._from == 'cm':
            return self._value * 2.54
        else:
            return None
