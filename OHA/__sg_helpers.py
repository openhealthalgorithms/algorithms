from OHA.Defaults import Defaults
from OHA.__unit import convert_height_unit
import numpy as np
import pandas as pd
'''
	__sg_helpers
    Formulas derived from the 2011 Guidelines from the SG MoH
'''

def find_age_index(age, age_brackets):    
    for age_range in age_brackets:
        min, max = age_range.split('-')
        if ((age > int(min)) & (age < int(max))):
            age_index = age_range
            return age_index
    
def age_modifier_fre_points(age, gender):
    
    age_brackets = ['20-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79']
    age_points = {
    	"male" : [-9, -4, 0, 3, 6, 8, 10, 11, 12, 13],
    	"female" : [-7, -3, 0, 3, 6, 8, 10, 12, 14, 16]
    } 

    index = 0
    value = None

    bracket = find_age_index(age, age_brackets)
    index = age_brackets.index(bracket)
    
    if index >= 0:
        value = age_points[gender][index]
    
    return value          
    
def calculate_smoking_points(age, gender):

    age_brackets = ['20-39', '40-49', '50-59', '60-69', '70-79']
    smoking_points = {
        "male" : [8, 5, 3, 1, 0],
        "female" : [9, 7, 4, 2, 1]
    }

    # Based on the age, look up the index
    # For the given index in the points array return the value
    
    index = 0
    value = None

    bracket = find_age_index(age, age_brackets)
    index = age_brackets.index(bracket)
    # should check we have a valid index
    if index >= 0:
        value = smoking_points[gender][index]
        print(value)
    
    return value    

def calculate_cholesterol_points(age, gender, total_cholesterol, hdl_cholesterol):
    
    age_brackets = ['20-39', '40-49', '50-59', '60-69', '70-79']
    
    if gender == 'male':
    	chol_points = np.array([[0, 0, 0, 0, 0], [4, 3, 2, 1, 0], [7, 5, 3, 1, 0], [9, 6, 4, 2, 1], [11, 8, 5, 3, 1]])
    elif gender == 'female':
    	chol_points = np.array([[0, 0, 0, 0, 0], [4, 3, 2, 1, 1], [8, 6, 4, 2, 1], [11, 8, 5, 3, 2], [13, 10, 7, 4, 2]])
    
    row_names = ['<4.1', '4.1-5.1', '5.2-6.1', '6.2-7.2','>=7.3']
    
    tchol_points_df = pd.DataFrame(chol_points, index=row_names, columns=age_brackets)
        
    # first check the cholesterol range and get the row_index
    
    if total_cholesterol < 4.1:
        chol_range = '<4.1'
    elif total_cholesterol <= 5.1:
        chol_range = '4.1-5.1'
    elif total_cholesterol <= 6.1:
        chol_range = '5.2-6.1'
    elif total_cholesterol <= 7.2:
        chol_range = '6.2-7.2'
    elif total_cholesterol >= 7.3:
        chol_range = '>=7.3'

    # then return the column index based on age range
    age_index = find_age_index(age, age_brackets)

    # look up the value from the df
    # looking up with keys 
    cholesterol_points = tchol_points_df[age_index][chol_range]
    
    if hdl_cholesterol < 1.0:
        hdl_points = +2
    elif hdl_cholesterol <= 1.2:
        hdl_points = 1
    elif hdl_cholesterol <= 1.5:
        hdl_points = 0
    elif hdl_cholesterol >= 1.6:
        hdl_points = -1
                
    cholesterol_points = cholesterol_points + hdl_points
    
    return cholesterol_points

def calculate_bp_points(gender, sbp, sbp_rx):
    
    row_names = ['<120', '120-129', '130-139', '140-159', '>=160']
    col_names = ['treated', 'untreated']
    
    if gender == 'male':
    	sbp_points = np.array([[0,0], [0,1], [1,2], [1,2], [2,3]])
    elif gender == 'female':
    	sbp_points = np.array([[0,0], [1,3], [2,4], [3,5], [4,6]])

    bp_df = pd.DataFrame(sbp_points, index=row_names, columns=col_names)
    
    if sbp < 120:
        spb_index = '<120'
    elif sbp < 130:
        sbp_index = '120-129'
    elif sbp < 140:
        sbp_index = '130-139'
    elif sbp < 160:
        sbp_index = '140-159'
    elif sbp >= 160:
        sbp_index = '>=160'
    
    if sbp_rx:
        col_index = 'treated'
    else:
        col_index = 'untreated'
    
    bp_points = bp_df[col_index][sbp_index]
    
    return bp_points

def calculate_fre_score(gender, ethnicity, points):
    
    col_names = ['chinese', 'malay', 'indian']
    if gender == 'male':
    	filename = 'OHA/sg_risk/sg_10year_risk_male.csv'
    else:
    	filename = 'OHA/sg_risk/sg_10year_risk_female.csv'
    
    fre_pd = pd.read_csv(filename, header=0, index_col=0)
    fre_risk = fre_pd[col_names]
    
    # look up the risk score based on the dataframe
    fre_risk_score = fre_risk[ethnicity][points]
    
    return fre_risk_score
    