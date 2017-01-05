#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:20:59 2016

@author: fredhersch
"""

import numpy as np
#import sys
#from sys import argv

#for arg in sys:
#    print (arg)
    
prompt = '> '

def convert_age(age):
    if (age <= 18):
        return 0
    elif (age <= 50):
        return 40
    elif (age <= 60):
        return 50
    elif (age <= 70):
        return 60
    elif (age <= 80):
        return 70
        
def convert_sbp(sbp):
    print "in function, sbp is %d " % (int(sbp))
    _sbp = int(sbp)
    if (_sbp <= 140):
        return 3
    elif ((_sbp > 140) & (_sbp <= 160)):
        return 2
    elif ((_sbp > 160) & (_sbp <= 180)):
        return 1
    elif (_sbp > 180):
        return 0

def convert_chol(chol):
    _chol = float(chol)
    print "in function, chol is %r " % (_chol)
    if (_chol <= 4.0):
        return 0
    elif ((_chol > 4.0) & (_chol <= 5.0)):
        return 1
    elif ((_chol > 5.0) & (_chol <= 6.0)):
        return 2
    elif ((_chol > 6.0) & (_chol <= 7.0)):
        return 3
    elif ((_chol > 7.0) & (_chol <= 8.0)):
        return 4

def convert_risk(result):
    _result = int(result)
    if _result == 10:
        risk_level = "<10%"
        risk_color = "Green"
        output_message = "You are at low risk. Counsel on diet, physical activity, smoking cessation and avoiding harmful use of alcohol"
        follow_up_interval = "12 months"
        targets = ""
#        return "<10%"
    elif _result == 20:
#        return "10-20%"
        risk_level = "10-20%"
        risk_color = "Yellow"
        output_message = "You are at increased risk. Counsel on diet, physical activity, smoking cessation and avoiding harmful use of alcohol"
        follow_up_interval = "3 months"
    elif _result == 30:
#        return "20-30%"
        risk_level = "20-30%"
        risk_color = "Amber"
        output_message = "You are at moderate risk. Counsel on diet, physical activity, smoking cessation and avoiding harmful use of alcohol. If persistent BP => 140/90 mmHg, consider anti-hypertensive therapy"
        follow_up_interval = "3-6 months"
    elif _result == 40:
#        return "30-40%"
        risk_level = "30-40%"
        risk_color = "Red"
        output_message = "You are at high risk. Counsel on diet, physical activity, smoking cessation and avoiding harmful use of alcohol. If persistent BP => 130/80 mmHg, consider anti-hypertensive therapy. Start a statin. Follow-up every 3 months, if there is no reduction in cardiovascular risk after six months of follow up refer to next level"
        follow_up_interval = "3 months"
    elif _result == 50:
#        return "> 40%"
        risk_level = ">40%"
        risk_color = "Marone"
        output_message = "You are at very high risk. Counsel on diet, physical activity, smoking cessation and avoiding harmful use of alcohol. If persistent BP => 130/80 mmHg, consider anti-hypertensive therapy. Start a statin. Follow-up every 3 months, if there is no reduction in cardiovascular risk after six months of follow up refer to next level"
        follow_up_interval = "3 months"
    return risk_level, risk_color, output_message, follow_up_interval

def check_high_risk(args):
    return true

# prompt for the raw_raw_input variables
print """ \n\nWelcome to your Health Assessment. Let's get started\n\n """

print "Do you have access to cholesterol data (Y or N)?",
s = raw_input(prompt)

if s.upper() == "Y":
    hasChol = 'YES'
    chol = 'c'
elif s.upper() == "N":
    hasChol = 'NO'
    #changed this to use an imputed value as per HEARTS guidelines
    chol = 'c'
else:
    print "Sorry I don't recognise that"   
        
print "Enter age",
_age = int(raw_input(prompt))
age = convert_age(_age)
if (age == 0):
    print "You must be over 18 .. using 40"
    age = 40
else:
    print "Ok, you entered age %d, that has been set at %d " % (_age, age)

print "Enter gender (M or F)",
s = raw_input(prompt)
gender = s.lower()

print "Do you have diabetes (Y or N)?",
d = raw_input(prompt)

if d.upper() == "Y":
    diabetes = "TRUE"
    dm = 'd'
elif d.upper() == "N":
    diabetes = "FALSE"
    dm = 'ud'
else:
    print "Sorry I don't recognise that entry"
    
print "Do you smoke? Or have you quit in the last 1 year? (y or n)",
s = raw_input(prompt)

if s.upper() == "Y":
    smoker = 's'
else:
    smoker = 'ns'

print (""" 
       Thanks, that's great. Now for some measurements
       """)

print "Please enter the first systolic blood pressure reading (that's the top number)"
sbp1 = int(raw_input(prompt))    
# should validate this

print "Please enter the second systolic blood pressure reading (that's the top number)"
sbp2 = int(raw_input(prompt))    

fn = lambda x, y: (x + y)/2

sbpAvg = fn(sbp1, sbp2)

sbpIndex = convert_sbp(sbpAvg)

print "Ok, your average SBP is %r which corresponds to %s " % (sbpAvg, sbpIndex) 

if hasChol == "YES":
    print "Let's get the cholesterol data. Enter in the total cholesterol in mmol/L",
    c = raw_input(prompt)
    cholIndex = convert_chol(c)
    print "Ok, your total cholesterol is %r which corresponds to %s " % (c, cholIndex) 
else:
    print "Without cholesterol the assessment will be less accurate. We will use an average of 5.2"
    c = 5.2


path = '/Users/fredhersch/Development/cvdrisk/WHOfiles/'
sbp = sbpIndex #represent ranges to be converted
tchol = cholIndex # represeent ranges to be converted

# work out which file to import
filename = chol + "_" + dm + "_" + gender + "_" + smoker + "_" + str(age) + ".txt"
print(filename)

# pick up the correct file to read
data = np.loadtxt(path + filename, dtype='string', delimiter=',')

print(data)

# based on sbp and tchol, read the risk score off the matrix
if chol == 'uc':
    value = data[sbp]
else:
    print "looking for index %r, %r" % (sbp, tchol)
    value = data[sbp, tchol]
    risk_score, risk_level, message, follow_up = convert_risk(value)

print "Based on the data provided, your risk color is %r, which equates to a 10 year cardiovascular risk of %s.\n\n%s.\nYou will need to be followed up in: %s " % (risk_level, risk_score, message, follow_up)
    
