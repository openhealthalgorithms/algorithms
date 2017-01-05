#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 19:13:36 2017

@author: fredhersch
"""

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