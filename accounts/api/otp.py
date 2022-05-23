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
        print("OTP", otp)
        sms_send_url = settings.OTP_SEND_URL
        params = {
            "auth_token": settings.OTP_SMS_TOKEN,
            "to": phone,
            "text": f"Your OTP is {otp}",
        }
        otp_send = requests.post(sms_send_url, data=params)
        result = otp_send.json()
        print("OTP SEND", result)
        if not result["error"]:
            return True
        return False
