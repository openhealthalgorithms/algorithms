#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from OHA.WHO import WHO
from OHA.param_builders.who_param_builder import WhoParamsBuilder as WPB


class WhoTest(unittest.TestCase):

    def test_should_produce_exception(self):
        params = WPB().gender('M').age(18).sbp1(130).sbp2(145).chol(5).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['exception'], 'color chart not found.')

        params = WPB().gender('M').age(100).sbp1(130).sbp2(145).chol(5).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['exception'], 'color chart not found.')

    def test_risk_is_10(self):
        params = WPB().gender('M').age(60).sbp1(130).sbp2(145).chol(4).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 10)

    def test_risk_is_20(self):
        params = WPB().gender('M').age(40).sbp1(130).sbp2(145).chol(7).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 20)

    def test_risk_is_30(self):
        params = WPB().gender('M').age(60).sbp1(180).sbp2(185).chol(4).build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 30)

    def test_risk_is_40(self):
        params = WPB().gender('M').age(70).sbp1(140).sbp2(150).chol(5).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 40)

    def test_risk_is_50(self):
        params = WPB().gender('F').age(80).sbp1(160).sbp2(180).chol(7).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 50)

        params = WPB().gender('F').age(80).sbp1(160).sbp2(180).chol(9).smoker().diabetic().build()
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 50)
