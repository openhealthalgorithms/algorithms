__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class WaistHipRatio(object):

    def __init__(self, waist=None, hip=None):
        self.__waist = waist
        self.__hip = hip

    def waist(self, waist):
        self.__waist = waist
        return self

    def hip(self, hip):
        self.__hip = hip
        return self

    @property
    def whr(self):
        return round(float(self.__waist / self.__hip), 2)
