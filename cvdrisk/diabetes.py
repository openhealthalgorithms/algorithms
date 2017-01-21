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

#def calcDiabetesStatus(*args):
    
"""
// Gender; F = 0, M = 2
// Age; if =<30 = 0, 31-40 = 3, >=41 = 4
// BMI; <25 = 0, >=25 = 2
// WHR; m < 0.9, f < 0.8 = 0; m >= 0.9, f >= 0.8 = 5
// HTN; SBP <140, DBP < 90 = 0; SBP >= 140, DBP >= 90 = 2
// If score >= 9/15, then should be further evaluated
"""

def calcWHR(waist, hip):
    whr = waist/hip
    print ("whr %s " % whr)
    return whr

def calcBMI(height, weight):
    bmi = weight/(height*height)
    print ("BMI is %s " % bmi)
    return bmi

def calcDiabetesRisk(gender, age, bmi, whr, sbp, dbp):

    risk_score = 0
    
    if gender == "M":
        risk_score = risk_score + 2
        if whr >= 0.9:
            risk_score = risk_score + 5
    else:
        if whr >= 0.8:
            risk_score = risk_score + 5
        
    if ((age > 30) & (age < 41)):
        risk_score = risk_score + 3
    elif age > 40:
        risk_score = risk_score + 4
    
    if bmi >= 25:
        risk_score = risk_score + 2
        
    # need to clarify this is it & or OR
    #  should be the average of two readings
    if ((sbp >= 140) or (dbp >= 90)):
        risk_score = risk_score + 2
    
    return risk_score

"""
Sample data
"""    
gender = "F"
age = 30
height = 1.5
weight = 70.0
waist = 99.0
hip = 104.0
sbp = 145
dbp = 80

diabetes_risk = calcDiabetesRisk(gender, age, calcBMI(height, weight), calcWHR(waist, hip), sbp, dbp)

print ("Risk is %s " % diabetes_risk)

    