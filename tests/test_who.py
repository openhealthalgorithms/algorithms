#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from nose_parameterized import parameterized

from OHA.WHO import WHO
from OHA.param_builders.who_param_builder import WhoParamsBuilder
from tests.helpers.DataHelper import DataHelper


class WhoTest(unittest.TestCase):

    def test_should_produce_exception(self):
        params = WhoParamsBuilder().gender('M').age(18).sbp1(130).sbp2(145).chol(5).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['exception'], 'color chart not found.')

        params = WhoParamsBuilder().gender('M').age(100).sbp1(130).sbp2(145).chol(5).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['exception'], 'color chart not found.')

    @parameterized.expand(DataHelper.who_test_data())
    def test_who_algorithm(self, region, age, gender, bp, total_chol, smoker, diabetes, cvd_risk):
        params = WhoParamsBuilder() \
            .region(region) \
            .gender(gender). \
            age(age). \
            sbp1(bp). \
            sbp2(bp). \
            chol(total_chol). \
            smoker(smoker == 1). \
            diabetic(diabetes == 1) \
            .build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk_range'], cvd_risk)
