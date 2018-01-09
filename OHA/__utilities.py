def calculate_bmi(weight, height):
    body_mass_index = weight / (height * height)
    return body_mass_index


def calculate_waist_hip_ratio(waist, hip):
    waist_hip_ratio = waist / hip
    return waist_hip_ratio


def cvd_risk_string(cvd_risk):
    if cvd_risk == 10:
        return '<10'
    elif cvd_risk == 20:
        return '10-20'
    elif cvd_risk == 30:
        return '20-30'
    elif cvd_risk == 40:
        return '30-40'
    elif cvd_risk == 50:
        return '>40'
    else:
        return '>40'

def load_guideline_content():
    file = 'guidelines/guideline_content.json'
    with open(file) as json_data:
        data = json.load(json_data) 

    return data

def load_guidelines(guideline_key):
    file = 'guidelines/guideline_hearts.json'
    with open(file) as json_data:
        data = json.load(json_data)
    return data

def output_messages(section, key, output_level=1):
    ''' return the relevant message based on the section, key and output_level'''
    ''' message is of the format key: [return_code, context, status, message] '''
    ''' output_level = 0 // return the key only
        output_level = 1 // return key and code
        output_level = 2 // key, code, context
        output_level = 3 // key, code, context, status
        output_level = 4 // key, code, context, status, message
    '''

    #load message - shift this to a separate package
    data = []
    messages = load_guideline_content()["body"]["messages"]
    content = messages[section]

    if output_level == 0:
        return key
    elif output_level == 1:
        data = [key, content[key][0]]
        return data
    elif output_level == 2:
        data = [key, content[key][0:2]]
        return data
    elif output_level == 3:
        data = [key, content[key][0:3]]
        return data
    elif output_level == 4:
        data = [key, content[key][0:4]]
        return data