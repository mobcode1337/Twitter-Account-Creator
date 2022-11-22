import requests, json

#   mine API Key = RPJdA9gqP8uMV0XExCMlCMdvSZb0rG

class PhoneVerification(object):
    api_key=None

    def __init__(self, api_key):
        self.api_key = api_key

    def get_balance(self):
        res = json.loads(requests.get(f"http://smspva.com/priemnik.php?metod=get_balance&service=opt4&apikey={self.api_key}").text)
        if res["response"] == "error":
            return {"balance": res["error_msg"]}
        if res["response"] == "1":
            return {"balance": res["balance"]}
        return {"balance": "something went wrong :/"}

    #   it uses Russian country and opt41 which is for Twitter
    def get_number(self):
        try:
            res = json.loads(requests.get(f"http://smspva.com/priemnik.php?metod=get_number&country=ES&service=opt41&apikey={self.api_key}").text)
            number = res["number"]
            _id = res["id"]
            return number, _id
        except:
            return "error_number", "error_id"
        
    def get_sms(self, _id):
        try:
            res = json.loads(requests.get(f"http://smspva.com/priemnik.php?metod=get_sms&country=ES&service=opt41&id={_id}&apikey={self.api_key}").text)
            if res["sms"] != None:
                return res["sms"]
        except:
            return "error_code"