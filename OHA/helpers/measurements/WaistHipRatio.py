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


if __name__ == '__main__':
    for mes in [[90, 100, 0.9], [100, 150, 0.67], [90, 100, 0.9], [80, 98, 0.82]]:
        bmi = WaistHipRatio(mes[0], mes[1]).whr
        print(f'waist => {mes[0]} \t hip => {mes[1]}  \twhr => {bmi}  \t {"PASS" if bmi == mes[2] else "FAIL"}')
