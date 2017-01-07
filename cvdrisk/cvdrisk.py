#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:20:59 2016

@author: fredhersch
"""

import numpy as np

# import sys
# from sys import argv

# for arg in sys:
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
    print ("in function, sbp is %d " % (int(sbp)))
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
    print ("in function, chol is %r " % (_chol))
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
    print(result)
    _result = result
    if _result == "10":
        return "<10%"
    elif _result == "20":
        return "10-20%"
    elif _result == "30":
        return "20-30%"
    elif _result == "40":
        return "30-40%"
    elif _result == "50":
        return "> 40%"


# prompt for the input variables
print (""" --- Welcome to your Health Assessment. Let's get started ---- """)

print ("Do you have access to cholesterol data (Y or N)?"),
s = raw_input(prompt)

if s.upper() == "Y":
    hasChol = 'YES'
    chol = 'c'
elif s.upper() == "N":
    hasChol = 'NO'
    # changed this to use an imputed value as per HEARTS guidelines
    chol = 'c'
else:
    print ("Sorry I don't recognise that")

print ("Enter age"),
_age = int(raw_input(prompt))
age = convert_age(_age)

print ("Enter gender (M or F)"),
s = raw_input(prompt)
gender = s.lower()

# print "So you have cholesterol data, %s , and your age is %s" % (chol, age, )

# print """Great, let's continue. Just a couple more questions"""

print ("Do you have diabetes (Y or N)?"),
d = raw_input(prompt)

if d.upper() == "Y":
    diabetes = "TRUE"
    dm = 'd'
elif d.upper() == "N":
    diabetes = "FALSE"
    dm = 'ud'
else:
    print ("Sorry I don't recognise that entry")

print ("Do you smoke? Or have you quit in the last 1 year? (y or n)"),
s = raw_input(prompt)

if s.upper() == "Y":
    smoker = 's'
else:
    smoker = 'ns'

print (""" 
       Thanks, that's great. Now for some measurements
       """)

print ("Please enter the first systolic blood pressure reading (that's the top number)")
sbp1 = int(raw_input(prompt))
# should validate this

print ("Please enter the second systolic blood pressure reading (that's the top number)")
sbp2 = int(raw_input(prompt))

fn = lambda x, y: (x + y) / 2

sbpAvg = fn(sbp1, sbp2)

sbpIndex = convert_sbp(sbpAvg)

print ("Ok, your average SBP is %r which corresponds to %s " % (sbpAvg, sbpIndex))

if hasChol == "YES":
    print ("Let's get the cholesterol data. Enter in the total cholesterol in mmol/L"),
    c = raw_input(prompt)
    cholIndex = convert_chol(c)
    print ("Ok, your total cholesterol is %r which corresponds to %s " % (c, cholIndex))
else:
    print ("Without cholesterol the assessment will be less accurate. We will use an average of 5.2")
    c = 5.2
    cholIndex = convert_chol(c)

path = 'WHOfiles/'
# write function to determine these based on the input values
# chol = 'c'
# dm = 'ud'
# gender = 'm' #alt 'f'
# smoker = 's' #alt 'ns'
# age = 50
sbp = sbpIndex  # represent ranges to be converted
tchol = cholIndex  # represeent ranges to be converted

# work out which file to import
filename = chol + "_" + dm + "_" + gender + "_" + smoker + "_" + str(age) + ".txt"
print(filename)

# pick up the correct file to read
data = np.loadtxt(path + filename, dtype=str, delimiter=',')

print(data)

# based on sbp and tchol, read the risk score off the matrix
if chol == 'uc':
    value = data[sbp]
else:
    print ("looking for index %d, %d" % (sbp, tchol))
    value = data[sbp, tchol]

print ("Based on the data provided, your result is %s, which equates to a 10 year cardiovascular risk of %s" % (
value, convert_risk(value)))
# print(value)
