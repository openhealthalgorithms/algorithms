#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import unittest

from OpenHealthAlgorithms.Diabetes import Diabetes


class DiabetesTest(unittest.TestCase):

    def test_risk_score_should_be_0(self):
        params = {'gender': 'F', 'age': 20, 'systolic': 139, 'diastolic': 89,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 0)

    def test_risk_score_should_be_2(self):
        params = {'gender': 'M', 'age': 20, 'systolic': 139, 'diastolic': 89,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 2)

    def test_risk_score_should_be_4(self):
        params = {'gender': 'M', 'age': 20, 'systolic': 139, 'diastolic': 90,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 4)

        params = {'gender': 'M', 'age': 20, 'systolic': 140, 'diastolic': 100,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 4)

        params = {'gender': 'M', 'age': 20, 'systolic': 140, 'diastolic': 89,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 4)

        params = {'gender': 'F', 'age': 42, 'systolic': 139, 'diastolic': 89,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 4)

    def test_risk_score_should_be_7(self):
        params = {'gender': 'M', 'age': 31, 'systolic': 139, 'diastolic': 90,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 7)

        params = {'gender': 'M', 'age': 31, 'systolic': 140, 'diastolic': 100,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 7)

        params = {'gender': 'M', 'age': 31, 'systolic': 140, 'diastolic': 89,
                  'weight': 50.0, 'height': 2.0, 'waist': 50.0, 'hip': 90.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 7)

    def test_risk_score_should_be_9(self):
        params = {'gender': 'F', 'age': 30, 'systolic': 145, 'diastolic': 80,
                  'weight': 70.0, 'height': 1.5, 'waist': 99.0, 'hip': 104.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 9)

    def test_risk_score_should_be_11(self):
        params = {'gender': 'M', 'age': 30, 'systolic': 145, 'diastolic': 80,
                  'weight': 70.0, 'height': 1.5, 'waist': 99.0, 'hip': 104.0}
        result = Diabetes().calculate(params)
        self.assertEqual(result['risk_score'], 11)
