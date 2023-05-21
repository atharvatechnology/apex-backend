import base64

import pyotp
import requests
from django.conf import settings
from django.utils.timezone import datetime

from accounts.tasks import send_otp


class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + settings.SECRET_KEY


class OTP:
    @staticmethod
    def __sendOTPAakash(to, otp):
        return {
            "auth_token": settings.OTP_SMS_TOKEN,
            "to": to,
            "text": f"Your OTP is {otp}",
        }

    @staticmethod
    def __sendOTPSparrow(to, otp):
        return {
            "token": settings.OTP_SMS_TOKEN,
            "from": settings.OTP_SMS_FROM,
            "to": to,
            "text": f"Your OTP is {otp}",
        }

    @staticmethod
    def __creditOTPAakash():
        return {
            "auth_token": settings.OTP_SMS_TOKEN,
        }

    @staticmethod
    def __creditOTPSparrow():
        return {
            "token": settings.OTP_SMS_TOKEN,
        }

    message_function = {
        "AakashSMS": {
            "send": __sendOTPAakash,
            "credit": __creditOTPAakash,
        },
        "SparrowSMS": {
            "send": __sendOTPSparrow,
            "credit": __creditOTPSparrow,
        },
    }

    @staticmethod
    def getOTP(phone):
        keygen = GenerateKey().returnValue(phone)
        key = base64.b32encode(keygen.encode())
        return pyotp.HOTP(key)

    @staticmethod
    def generateOTP(phone, counter):
        otp = OTP().getOTP(phone)
        return otp.at(counter)

    @staticmethod
    def verifyOTP(phone, counter, otp):
        generate_otp = OTP().getOTP(phone)
        return bool(generate_otp.verify(otp, counter))

    @staticmethod
    def sendOTP(phone, otp):
        sms_send_url = settings.OTP_SEND_URL
        platform = settings.OTP_SMS_PLATFORM
        if platform in OTP().message_function:
            params = OTP().message_function[platform]["send"](phone, otp)
            send_otp.delay(sms_send_url, params, platform)
            # otp_send = requests.post(sms_send_url, data=params)

        # if platform == "AakashSMS":
        #     result = otp_send.json()
        #     if not result["error"]:
        #         return True
        # elif platform == "SparrowSMS":
        #     if otp_send.status_code == 200:
        #         return True
        # TODO: Remove this line if possible
        return True

    @staticmethod
    def getCredit():
        sms_credit_url = settings.OTP_CREDIT_URL
        platform = settings.OTP_SMS_PLATFORM
        if platform in OTP().message_function:
            params = OTP().message_function[platform]["credit"]()
        if platform == "AakashSMS":
            otp_credit = requests.post(sms_credit_url, data=params)
            result = otp_credit.json()
            if not result["error"]:
                return {"credit": result["available_credit"]}
        elif platform == "SparrowSMS":
            otp_credit = requests.get(sms_credit_url, params=params)
            if otp_credit.status_code == 200:
                return {"credit": otp_credit.json()["credits_available"]}
        return {"credit": False}
