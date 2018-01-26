__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class CaloricIntake(object):
    def __init__(self, gender=None, weight=None, height=None, age=None, physical_activity_level=None):
        self.__gender = gender
        self.__weight = weight
        self.__height = height
        self.__age = age
        self.__physical_activity_level = physical_activity_level

    def gender(self, gender):
        self.__gender = gender

    def weight(self, weight):
        self.__weight = weight

    def height(self, height):
        self.__height = height

    def age(self, age):
        self.__age = age

    def physical_activity_level(self, physical_activity_level):
        self.__physical_activity_level = physical_activity_level

    @property
    def ci(self):
        """
        Using the Revised Harris-Benedict Equation
        Men BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) - (5.677 x age in years)
        Women BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) - (4.330 x age in years)
        """

        # ensure the height, weight are in the correct units
        # currently assuming so

        if self.__gender == 'M':
            bmr = 88.362 + (13.397 * self.__weight) + (4.7999 * self.__height) - (5.677 * self.__age)
        elif self.__gender == 'F':
            bmr = 447.593 + (9.247 * self.__weight) + (3.098 * self.__height) - (4.330 * self.__age)
        else:
            bmr = 447.593 + (9.247 * self.__weight) + (3.098 * self.__height) - (4.330 * self.__age)

        activity_multiplier = 1.0

        if self.__physical_activity_level == 0:
            activity_multiplier = 1.2
        elif self.__physical_activity_level == 1:
            activity_multiplier = 1.375
        elif self.__physical_activity_level == 2:
            activity_multiplier = 1.55
        elif self.__physical_activity_level == 3:
            activity_multiplier = 1.725
        elif self.__physical_activity_level == 4:
            activity_multiplier = 1.9

        caloric_intake = bmr * activity_multiplier

        return caloric_intake
