import requests
from celery import shared_task


@shared_task
def send_otp(sms_send_url, params, platform):
    """Send OTP to the user."""
    otp_send = requests.post(sms_send_url, data=params)
    if platform == "AakashSMS":
        result = otp_send.json()
        if not result["error"]:
            return True
    elif platform == "SparrowSMS":
        if otp_send.status_code == 200:
            return True
    return "OTP was not send"
