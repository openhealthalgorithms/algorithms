class BMI(object):

    def __init__(self, weight=None, height=None):
        self.__weight = weight
        self.__height = height

    def weight(self, weight):
        self.__weight = weight
        return self

    def height(self, height):
        self.__height = height
        return self

    @property
    def bmi(self):
        return round(float(self.__weight / (self.__height ** 2)), 2)
