#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import numpy as np

from OHA.__unit import convert_cholesterol_unit
from OHA.helpers.formatters.ParamFormatter import ParamFormatter
from OHA.param_builders.framingham_param_builder import FraminghamParamsBuilder

__author__ = 'fredhersch'
__email__ = 'fred@openhealthalgorithms.org'

'''
    Class for BaseAssessment
    All Assessments Inherit the BaseAssessment Class
    A BaseAssessment has a:
        Status
        Targets 
'''

class BaseAssessment(object):

    def __init__(self):
