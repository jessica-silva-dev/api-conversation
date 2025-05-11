import re

class ValidatePhone:
    
    @staticmethod
    def validate_phone_number(phonenumber):
        
        phonenumber_edit = re.sub(r'\D', '', phonenumber)
        
        if not phonenumber_edit.startswith('55'):
            return phonenumber_edit
        
        if len(phonenumber_edit) == 13 and phonenumber_edit[4] == '9':
            return phonenumber_edit
        
        if len(phonenumber_edit) == 12:
            ninth_digit = phonenumber_edit[:4] + '9' + phonenumber_edit[4:]
            return ninth_digit
        