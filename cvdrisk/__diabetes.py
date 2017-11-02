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