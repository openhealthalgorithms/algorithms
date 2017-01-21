#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 17:47:55 2017

@author: fredhersch
"""

"""
This module will be used to calculate the status of diabetes in UNKNOWN
If a person has diabetes in their past history, that should be passed into relevant algorithms
Currently we are using the Diabetes Risk Score from CGHR
Assessment of Diabetes Status is based on IDF / WHO Hearts Guidelines

Steps:
    
    1. Determine whether there is any pathology
    2. If pathology, then attempt to calculate diabetes status
        - Suspected => has a fasting BSL > 7.1 or a random > 11.1, HbA1c of > 6.5 - Needs to be repeated
        - Impaired => has impaired fasting glucose or impaired glucose tolerance. At risk of diabetes. Should be confirmed; BSL > 7.1 AND < 11.1, HbA1c 5.7-6.4
        - Normal => BSL is within normal range, HbA1c < 5.7
    3. If no pathology, then attempt to calculate risk score using the appropriate algorithm
    
"""

def calcDiabetesStatus(*args):
    