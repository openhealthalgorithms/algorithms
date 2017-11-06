from OHA.__utilities import calculate_bmi

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'


class HEARTS(object):
    """

    """

    @staticmethod
    def assess_bmi(height, weight):
        _assessment = False
        _assessment_code = None
        _target = "18.5 - 24.9"
        _target_message = ""

        bmi = calculate_bmi(weight[0], height[0])

        if bmi < 18.5:
            _assessment = True
            _assessment_code = "UW"
            # return (True, 'AMBER', 'UW', bmi)
        elif bmi < 25:
            _assessment = False
            _assessment_code = "NW"
            # return (False, 'GREEN', 'NW', bmi)
        elif bmi < 30:
            _assessment = True
            _assessment_code = "OW"
            # return (True, 'AMBER', 'OW', bmi)
        else:
            _assessment = True
            _assessment_code = "OB"
            # return (True, 'RED', 'OB', bmi)
        # return bmi

        bmi_output = {
            'value': bmi,
            'assessment_code': _assessment_code,
            'target': _target,
            'target_message': _target_message
        }

        return bmi_output
