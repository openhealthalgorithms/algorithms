import abc

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class BaseConverter(abc.ABC):
    def __init__(self, _value, _from=None, _to=None):
        self.__from = _from
        self.__to = _to
        self.__value = _value
        self.__exception = list()

    @property
    def _from(self):
        if self.__from is None:
            return self._default_from_unit().lower()
        return self.__from.lower()

    @property
    def _to(self):
        if self.__to is None:
            return self._default_to_unit().lower()
        return self.__to.lower()

    @property
    def _value(self):
        return self.__value

    def from_unit(self, value=None):
        self.__from = value
        return self

    def to_unit(self, value=None):
        self.__to = value
        return self

    @abc.abstractmethod
    def _default_from_unit(self):
        raise NotImplementedError('method not implemented')

    @abc.abstractmethod
    def _default_to_unit(self):
        raise NotImplementedError('method not implemented')

    def __validate_values(self):
        if self._from not in self._from_values():
            self.__exception.append('"{_from}" is not allowed as "from" value.'.format(_from=self.__from))
        if self._to not in self._to_values():
            self.__exception.append('"{_to}" is not allowed as "to" value.'.format(_to=self.__to))

    @abc.abstractmethod
    def _from_values(self) -> list:
        raise NotImplementedError('method not implemented')

    @abc.abstractmethod
    def _to_values(self) -> list:
        raise NotImplementedError('method not implemented')

    @abc.abstractmethod
    def _convert(self):
        raise NotImplementedError('method not implemented')

    @property
    def converted(self):
        self.__validate_values()
        if len(self.__exception) > 0:
            raise ValueError(', '.join(self.__exception))
        return self._convert()
