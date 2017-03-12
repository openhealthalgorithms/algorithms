#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from OpenHealthAlgorithms.WHO import WHO


class FraminghamTest(unittest.TestCase):
    def test_should_produce_exception(self):
        params = {
            'gender': "M",
            'age': 18,
            'systolic_blood_pressure_1': 130,
            'systolic_blood_pressure_2': 145,
            'cholesterol': 5,
            'is_smoker': "Y",
            'has_diabetes': "Y",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['exception'], 'file not found')

        params = {
            'gender': "M",
            'age': 100,
            'systolic_blood_pressure_1': 130,
            'systolic_blood_pressure_2': 145,
            'cholesterol': 5,
            'is_smoker': "Y",
            'has_diabetes': "Y",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['exception'], 'file not found')

    def test_risk_is_10(self):
        params = {
            'gender': "M",
            'age': 60,
            'systolic_blood_pressure_1': 130,
            'systolic_blood_pressure_2': 145,
            'cholesterol': 4,
            'is_smoker': "Y",
            'has_diabetes': "Y",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 10)

    def test_risk_is_20(self):
        params = {
            'gender': "M",
            'age': 40,
            'systolic_blood_pressure_1': 130,
            'systolic_blood_pressure_2': 145,
            'cholesterol': 7,
            'is_smoker': "Y",
            'has_diabetes': "Y",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 20)

    def test_risk_is_30(self):
        params = {
            'gender': "M",
            'age': 60,
            'systolic_blood_pressure_1': 180,
            'systolic_blood_pressure_2': 185,
            'cholesterol': 4,
            'is_smoker': "N",
            'has_diabetes': "N",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 30)

    def test_risk_is_40(self):
        params = {
            'gender': "M",
            'age': 70,
            'systolic_blood_pressure_1': 140,
            'systolic_blood_pressure_2': 150,
            'cholesterol': 5,
            'is_smoker': "Y",
            'has_diabetes': "Y",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 40)

    def test_risk_is_50(self):
        params = {
            'gender': "F",
            'age': 80,
            'systolic_blood_pressure_1': 160,
            'systolic_blood_pressure_2': 180,
            'cholesterol': 7,
            'is_smoker': "Y",
            'has_diabetes': "Y",
        }
        result = WHO().calculate(params)
        self.assertEqual(result['risk'], 50)
