import abc

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class Assessment(abc.ABC):
    __data = {}

    def __init__(self, input_data=None):
        if input_data is not None:
            if input_data['gender'] not in ["F", "M"]:
                raise ValueError('gender value must be "F" or "M"')
            self.__data = input_data

    def _get_data(self):
        return self.__data

    @abc.abstractmethod
    def assess(self):
        pass
