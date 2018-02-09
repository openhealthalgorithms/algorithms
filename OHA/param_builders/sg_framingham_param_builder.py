__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class SGFraminghamParamsBuilder(object):
    def __init__(self):
        self.__gender = 'male'
        self.__ethnicity = 'chinese'
        self.__age = 40
        self.__sbp = 140
        self.__t_chol = None
        self.__t_chol_unit = 'mg/dl'
        self.__chol_unit = 'mmol/l'
        self.__hdl_chol = None
        self.__hdl_chol_unit = 'mg/dl'
        self.__bp_medication = False
        self.__smoker = False
        self.__diabetic = False

    def ethnicity(self, ethnicity):
        self.__ethnicity = ethnicity
        return self

    def gender(self, gender):
        self.__gender = gender
        return self

    def age(self, age):
        self.__age = age
        return self

    def sbp(self, sbp):
        self.__sbp = sbp
        return self

    def hdl_chol(self, hdl_chol, hdl_chol_unit='mg/dl'):
        self.__hdl_chol = hdl_chol
        self.__hdl_chol_unit = hdl_chol_unit
        return self

    def t_chol(self, t_chol, t_chol_unit='mg/dl'):
        self.__t_chol = t_chol
        self.__t_chol_unit = t_chol_unit
        return self

    def bp_medication(self, bp_medication=True):
        self.__bp_medication = bp_medication
        return self

    def smoker(self, smoker=True):
        self.__smoker = smoker
        return self

    def diabetic(self, diabetic=True):
        self.__diabetic = diabetic
        return self

    def build(self):
        return {
            'gender': self.__gender,
            'age': self.__age,
            'ethnicity': self.__ethnicity,
            'total_cholesterol': self.__t_chol,
            'total_cholesterol_unit': self.__t_chol_unit,
            'hdl_cholesterol': self.__hdl_chol,
            'hdl_cholesterol_unit': self.__hdl_chol_unit,
            'systolic': self.__sbp,
            'on_bp_medication': self.__bp_medication,
            'is_smoker': self.__smoker,
            'has_diabetes': self.__diabetic,
        }
