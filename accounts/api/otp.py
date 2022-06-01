import base64

import pyotp
import requests
from django.conf import settings
from django.utils.timezone import datetime


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

    message_function = {
        "AakashSMS": __sendOTPAakash,
        "SparrowSMS": __sendOTPSparrow,
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
        if generate_otp.verify(otp, counter):
            return True
        return False

    @staticmethod
    def sendOTP(phone, otp):
        sms_send_url = settings.OTP_SEND_URL
        platform = settings.OTP_SMS_PLATFORM
        if platform in OTP().message_function:
            params = OTP().message_function[platform](phone, otp)
            otp_send = requests.post(sms_send_url, data=params)
        if platform == "AakashSMS":
            result = otp_send.json()
            if not result["error"]:
                return True
        elif platform == "SparrowSMS":
            if otp_send.status_code == 200:
                return True
        return False
