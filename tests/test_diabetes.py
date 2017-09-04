#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from OHA.Diabetes import Diabetes
from OHA.param_builders.diabetes_param_builder import DiabetesParamsBuilder as DBP


class DiabetesTest(unittest.TestCase):

    def test_risk_is_0(self):
        params = DBP().gender("F").age(20).sbp(139).dbp(89).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 0)

    def test_risk_is_2(self):
        params = DBP().gender("M").age(20).sbp(139).dbp(89).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 2)

    def test_risk_is_4(self):
        params = DBP().gender("M").age(20).sbp(139).dbp(90).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 4)

        params = DBP().gender("M").age(20).sbp(140).dbp(100).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 4)

        params = DBP().gender("M").age(20).sbp(140).dbp(89).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 4)

        params = DBP().gender("F").age(42).sbp(139).dbp(89).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 4)

    def test_risk_is_7(self):
        params = DBP().gender("M").age(31).sbp(139).dbp(90).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 7)

        params = DBP().gender("M").age(31).sbp(140).dbp(100).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 7)

        params = DBP().gender("M").age(31).sbp(140).dbp(89).weight(50).height(2).waist(50).hip(90).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 7)

    def test_risk_is_9(self):
        params = DBP().gender("F").age(30).sbp(145).dbp(80).weight(70).height(1.5).waist(99).hip(104).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 9)

    def test_risk_is_11(self):
        params = DBP().gender("M").age(30).sbp(145).dbp(80).weight(70).height(1.5).waist(99).hip(104).build()
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk'], 11)
