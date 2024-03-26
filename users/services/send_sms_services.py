import phonenumbers, random, requests, json
from dotenv import dotenv_values
from urllib.parse import urlparse, urlunparse, urlencode

from users.enums import MessageStatus

class SendSmsServices:
    aero_url = dotenv_values('myproject/.env')['sms_aero']
    def __init__(self, phone_number:int) -> None:
        self.phone_number = phone_number


    def validate_number(self):
        try:
            parsed_number = phonenumbers.parse("+"+self.phone_number, None)
            return phonenumbers.is_valid_number(parsed_number) and phonenumbers.region_code_for_number(parsed_number) == 'RU'
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
    
    def sms_status(self, sms_id:int):
        end_point = "sms/teststatus"
        params = {"id":sms_id}
        encoded_params = urlencode(params)
        modified_url = f"{self.aero_url}{end_point}?{encoded_params}"
        response = requests.get(modified_url)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            status = response_dict["data"]["status"]
            return status
        return None

    def sms_lists(self):
        end_point = "sms/testlist"
        modified_url = f"{self.aero_url}{end_point}"
        response = requests.get(modified_url)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict
        
    def sms_send(self):
        end_point = "sms/testsend"

        validate = self.validate_number()
        
        if validate:
            send_obj = {
                'verify_code': None,
                'sms_status': '',
                'response_status': False,
                'sms_id': None,
                'sms_status_number': None
            }
            verify_code = random.randint(1000, 9999)
            send_obj['verify_code'] = verify_code
            params = {"number": self.phone_number, "text": str(verify_code), "sign":"SMS Aero"}
            encoded_params = urlencode(params)
            modified_url = f"{self.aero_url}{end_point}?{encoded_params}"
            response = requests.get(modified_url)
            if response.status_code == 200:
                sms_id = json.loads(response.text)["data"]["id"]
                send_obj['sms_id']=sms_id
                sm_stat = self.sms_status(sms_id=sms_id)
                message_status = MessageStatus.get_string_value(value=sm_stat) if sm_stat != None else False
                response_dict = json.loads(response.text)
                send_obj["sms_status_number"] = sm_stat
                send_obj['sms_status'] = message_status
                send_obj["response_status"] = True
            return send_obj    
        else:
            return False