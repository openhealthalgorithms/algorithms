from OHA.assessments.Assessment import Assessment

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class DietAssessment(Assessment):
    def __init__(self, input_data=None):
        super().__init__(input_data)

    def __diet_history(self):
        return self._get_data()['diet_history']

    def __diet_vegetable(self):
        return self.__diet_history()['veg']

    def __diet_fruit(self):
        return self.__diet_history()['fruit']

    def __targets(self):
        return self._get_data()['targets']

    def __target_vegetable(self):
        return self.__targets()['general']['diet']['vegetables']

    def __target_fruit(self):
        return self.__targets()['general']['diet']['fruit']

    def assess(self):
        if self.__diet_fruit() < self.__target_fruit() and self.__diet_vegetable() < self.__target_vegetable():
            result_code = 'NUT-3'
        elif (self.__diet_fruit() < self.__target_fruit()) and (self.__diet_vegetable() >= self.__target_vegetable()):
            result_code = 'NUT-2'
        elif (self.__diet_fruit() > self.__target_fruit()) and (self.__diet_vegetable() < self.__target_vegetable()):
            result_code = 'NUT-2'
        else:
            result_code = 'NUT-1'

        return dict(values=dict(fruit=self.__diet_fruit(), vegetables=self.__diet_vegetable()), code=result_code)
