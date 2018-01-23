import pandas


class DataHelper(object):
    @staticmethod
    def who_test_data():
        filename = 'tests/data/who_tests.csv'
        data = pandas.read_csv(filename)
        return data.values.tolist()
