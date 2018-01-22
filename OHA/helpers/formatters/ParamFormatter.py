class ParamFormatter(object):
    def __init__(self, params):
        self.__params = params

    @property
    def formatted(self):
        return {
            key: float(value) if type(value) is int else value
            for key, value in self.__params.items()
        }
