from decouple import config
from kavenegar import *


def send_top_code(phone_number, code):
    try:
        api = KavenegarAPI(config("API_KEY"))
        params = {
            "sender": config("sender_number"),
            "receptor": config("receptor"),
            "message": f"کد تایید شما: {code} گی دی خمینی سیصد بار",
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(f"API Error: {e}")
    except HTTPException as e:
        print(f"HTTP Error: {e}")
