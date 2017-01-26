#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from OpenHealthAlgorithms.Framingham import Framingham


class FraminghamTest(unittest.TestCase):
    def test_heart_age_and_actual_age_is_same(self):
        params = {
            'gender': 'F',
            'age': 40,
            'total_cholesterol': 180,
            'hdl_cholesterol': 45,
            'systolic': 125,
            'on_bp_medication': False,
            'is_smoker': False,
            'has_diabetes': False,
        }
        result = Framingham().calculate(params)
        self.assertEqual(result['heart_age'], params['age'])

    def test_heart_age_greater_than_actual_age(self):
        params = {
            'gender': 'F',
            'age': 40,
            'total_cholesterol': 280,
            'hdl_cholesterol': 45,
            'systolic': 125,
            'on_bp_medication': True,
            'is_smoker': True,
            'has_diabetes': True,
        }
        result = Framingham().calculate(params)
        self.assertGreater(result['heart_age'], params['age'])

    def test_heart_age_less_than_actual_age(self):
        params = {
            'gender': 'F',
            'age': 40,
            'total_cholesterol': 100,
            'hdl_cholesterol': 30,
            'systolic': 125,
            'on_bp_medication': False,
            'is_smoker': False,
            'has_diabetes': False,
        }
        result = Framingham().calculate(params)
        self.assertLess(result['heart_age'], params['age'])
