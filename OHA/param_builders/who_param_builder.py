class WhoParamsBuilder(object):
    def __init__(self):
        self.__gender = 'M'
        self.__age = 40
        self.__sbp1 = 140
        self.__sbp2 = 160
        self.__chol = 5
        self.__chol_unit = 'mmol/l'
        self.__smoker = False
        self.__diabetic = False
        self.__region = 'SEARD'

    def gender(self, gender):
        self.__gender = gender
        return self

    def age(self, age):
        self.__age = age
        return self

    def sbp1(self, sbp1):
        self.__sbp1 = sbp1
        return self

    def sbp2(self, sbp2):
        self.__sbp2 = sbp2
        return self

    def chol(self, chol, chol_unit='mmol/l'):
        self.__chol = chol
        self.__chol_unit = chol_unit
        return self

    def smoker(self, smoker=True):
        self.__smoker = smoker
        return self

    def diabetic(self, diabetic=True):
        self.__diabetic = diabetic
        return self

    def region(self, region):
        self.__region = region
        return self

    def build(self):
        return {
            'gender': self.__gender,
            'age': self.__age,
            'systolic_blood_pressure_1': self.__sbp1,
            'systolic_blood_pressure_2': self.__sbp2,
            'cholesterol': self.__chol,
            'cholesterol_unit': self.__chol_unit,
            'is_smoker': self.__smoker,
            'has_diabetes': self.__diabetic,
            'region': self.__region,
        }
