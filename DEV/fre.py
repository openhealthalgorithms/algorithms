#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 13:47:36 2017

@author: fredhersch
"""

import numpy as np;

#co-efficients used in the calculation. See relevant paper

defs = { "so10" : {'F':0.95012, 'M':0.8893}, 
  "logAge" : {'F':2.32888, 'M':3.06117},
  "logTChol" : {'F':1.20904, 'M':1.12370},
  "logHDLChol" : {'F':0.70833, 'M':0.93263},
  "logSBPNonRx" : {'F':2.76157, 'M':1.93303},
  "logSBPRx" : {'F':2.82263, 'M':1.99881},
  "logSmoking" : {'F':0.52873, 'M':0.65451},
  "logDM" : {'F':0.69154, 'M':0.57367},
  "calc_mean" : {'F':26.1931, 'M':23.9802}
}


"""
    Pass in variables:
    Gender: M, F
    Age: As integer
    TChol: Total Cholesterol
    hdl: HDL Cholesterol
    rx_bp: Medicaiton for BP, Boolean True or False
    sbp: systolic bp
    sbp_rx: treated sbp
    smoker: Boolean, True or False
    diabetes: boolean, True or False
    """

def calcFREScore(gender, age, tchol, hdl, rx_bp, sbp, smoker, diabetes):
    
    
    calc_1 = (defs["logAge"][gender] * np.log(age)) + defs["logTChol"][gender] * np.log(tchol) - defs["logHDLChol"][gender] * np.log(hdl)
    
    sbp_calc = 0
    
    #If on medication for BP
    if (rx_bp):
        print("on bp meds")
        sbp_calc = defs["logSBPRx"][gender] * np.log(sbp)
    else:
        print("not on meds")
        sbp_calc = defs["logSBPNonRx"][gender] * np.log(sbp)

    calc_2 = calc_1 + sbp_calc + (defs["logSmoking"][gender] * smoker) + (defs["logDM"][gender] * diabetes)

    fre = 1 - np.power(defs["so10"][gender], np.exp(calc_2 - defs["calc_mean"][gender]))
        
    return fre

"""
Calculate for what age the risk score is associated with using "normal" values of
Tchol 180, hdl 45, non-treated sbp 125, non smoker and not diabetic
"""
    
def calcHeartAge(cvd_risk, gender):
    
   age = 30
   heart_age = age
   print("CVD_Risk %s " % round(cvd_risk, 2))
   
   while (age < 100):
       age_risk = calcFREScore(gender, age, 180, 45, 0, 125, 0, 0)
       print("for age %s " % age + " risk is %s " % (round(age_risk, 2)*100))
       if (round(age_risk, 2) == round(cvd_risk, 2)):
           heart_age = age
           break
       else:
           age = age + 1
           continue
           
   return heart_age
         

"""
Test cases based on the paper
Change the gender to get the output
Expected to be:
    For M, risk 15.6% with Heart Age of 64
    For F, risk is 10.5% with Heart Age of 75 - Currently getting 10.7% - Need to check
    For the woman who smokes, we calculate her risk and heart age if she didn't smoke
"""    
gender = "F"
if gender == "M":
    age = 53
#calculateFREScore(gender, age, tchol, hdl, rx_bp, sbp, smoker, diabetes):
    cvd_risk = calcFREScore(gender, age, 161, 55, 1, 125, 0, 1)
#cvd_risk = calcFREScore(gender, 53, 161, 55, 1, 125, 0, 1)
else:
    age = 61
    cvd_risk = calcFREScore(gender, age, 180, 47, 0, 125, 1, 0)
    cvd_risk_non_smoker = calcFREScore(gender, age, 180, 47, 0, 125, 0, 0)
    heart_age_non_smoker = calcHeartAge(cvd_risk_non_smoker, gender)

age_risk = calcFREScore(gender, age, 180, 45, 0, 125, 0, 0)
heart_age = calcHeartAge(cvd_risk, gender)

print "cvd risk score is %.1f" % (cvd_risk*100) + "%"

print "\nOptimum risk for age is " + " %.1f" % (round(age_risk,3)*100) + "%"

print "\Heart Age is %s " % heart_age

if gender == "F":
    print "\nIf this %s years old woman quit smoking risk would be %s " % (age, round(cvd_risk_non_smoker,3)*100) + "%"
    print "\nGiving her a heart age of %s " % heart_age_non_smoker

