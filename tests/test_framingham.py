#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from OHA.Framingham import Framingham
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder as FPB


class FraminghamTest(unittest.TestCase):
    def test_heart_age_and_actual_age_is_same(self):
        params = FPB().gender("F").age(40).t_chol(180).hdl_chol(45).sbp(125).build()
        result = Framingham().calculate(params)
        self.assertEqual(result['heart_age'], params['age'])

    def test_heart_age_greater_than_actual_age(self):
        params = FPB().gender("F").age(40).t_chol(280).hdl_chol(45).sbp(125).bp_medication().smoker().diabetic().build()
        result = Framingham().calculate(params)
        self.assertGreater(result['heart_age'], params['age'])

    def test_heart_age_less_than_actual_age(self):
        params = FPB().gender("F").age(40).t_chol(100).hdl_chol(30).sbp(125).build()
        result = Framingham().calculate(params)
        self.assertLess(result['heart_age'], params['age'])
