import phonenumbers

class SendSmsServices:
    def __init__(self, aero_url: str, phone_number:int) -> None:
        self._aero_url = aero_url
        self.phone_number = phone_number

    def validate_number(self):
        try:
            parsed_number = phonenumbers.parse("+"+self.phone_number, None)
            return phonenumbers.is_valid_number(parsed_number) and phonenumbers.region_code_for_number(parsed_number) == 'RU'
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        
    def sms_send(self):
        validate = self.validate_number()
        if validate:
            pass
        else:
            return False