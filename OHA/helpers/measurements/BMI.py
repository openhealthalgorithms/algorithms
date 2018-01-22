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


if __name__ == '__main__':
    for mes in [[50, 60, 33.95], [55, 1.76, 32.28], [90, 1.8, 27.78], [65, 1.3, 38.46]]:
        bmi = BMI(mes[0], mes[1]).bmi
        print(f'weight => {mes[0]}\t height => {mes[1]}\t bmi => {bmi}\t {"PASS" if bmi == mes[2] else "FAIL"}')
