class DiabetesParamsBuilder(object):
    def __init__(self):
        self.__gender = 'M'
        self.__age = 40
        self.__sbp = 135
        self.__dbp = 145
        self.__weight = 70
        self.__weight_unit = 'kg'
        self.__height = 1.75
        self.__height_unit = 'm'
        self.__waist = 85
        self.__waist_unit = 'cm'
        self.__hip = 110
        self.__hip_unit = 'cm'

    def gender(self, gender):
        self.__gender = gender
        return self

    def age(self, age):
        self.__age = age
        return self

    def sbp(self, sbp):
        self.__sbp = sbp
        return self

    def dbp(self, dbp):
        self.__dbp = dbp
        return self

    def weight(self, weight, weight_unit='kg'):
        self.__weight = weight
        self.__weight_unit = weight_unit
        return self

    def height(self, height, height_unit='m'):
        self.__height = height
        self.__height_unit = height_unit
        return self

    def waist(self, waist, waist_unit='cm'):
        self.__waist = waist
        self.__waist_unit = waist_unit
        return self

    def hip(self, hip, hip_unit='cm'):
        self.__hip = hip
        self.__hip_unit = hip_unit
        return self

    def build(self):
        params = {
            'gender': self.__gender,
            'age': self.__age,
            'systolic': self.__sbp,
            'diastolic': self.__dbp,
            'weight': self.__weight,
            'weight_unit': self.__weight_unit,
            'height': self.__height,
            'height_unit': self.__height_unit,
            'waist': self.__waist,
            'waist_unit': self.__waist_unit,
            'hip': self.__hip,
            'hip_unit': self.__hip_unit,
        }

        return params
