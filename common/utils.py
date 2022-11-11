import os
from typing import Union

import segno
from django.conf import settings
from django.core import signing
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags

from apex.celery import app


def generate_qrcode(data):
    """Generate qr code for data.

    Parameters
    ----------
    data : str
        data to be encoded in qr code.
    file_path : str
        path to file

    """
    secret_generator = signing.Signer(salt=settings.SECRET_KEY)
    encripted_user = secret_generator.sign_object(data)
    qr_img = segno.make(encripted_user, micro=False)
    media_path = f"qr_code/{data}"
    base_path = os.path.join(settings.BASE_DIR, f"media/{media_path}")
    os.makedirs(base_path, exist_ok=True)
    qr_img.save(f"{base_path}/qr.svg", scale=10)
    return f"{media_path}/qr.svg"


def decode_user(email: str) -> Union[str, None]:
    """Return decrypted email and error if any."""

    signer = signing.Signer(salt=settings.SECRET_KEY)  # salt needs to be same
    try:
        return signer.unsign_object(email)
    except signing.BadSignature:
        return None


# def read_qrcode(file_path):
#     """Read the image and return the data.

#     Parameters
#     ----------
#     file_path : str
#         path to file

#     Returns
#     -------
#     _data: str
#         detect the qr code from img and return the data.
#     """

#     img = cv2.imread(file_path)
#     detector = cv2.QRCodeDetector()
#     data, bbox, straight_qrcode = detector.detectAndDecode(img)
#     return data


"""file contains utility functions for the project."""


def get_human_readable_date_time(data):
    """Get human readable date time."""
    return data.strftime("%Y-%m-%d %H:%M %p")


def send_mail_common(template, context, to, subject):
    htmly = get_template(template)
    from_email = settings.EMAIL_HOST_USER
    html_content = htmly.render(context)
    text_content = strip_tags(html_content)
    # msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    async_send_mail.delay(subject, text_content, from_email, to, html_content)


@app.task
def async_send_mail(subject, text_content, from_email, to, html_content):
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_random_string():
    import random
    import string

    return "".join(random.choice(string.ascii_letters) for _ in range(7))
