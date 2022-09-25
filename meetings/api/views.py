from time import time

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import GenerateSignatureSerializer


def generate_signature(data):
    iat = round(time()) - 30
    exp = iat + 60 * 60 * 2
    header_dict = {"alg": "HS256", "typ": "JWT"}
    zoom_conf = settings.ZOOM_CONFIGS
    zoom_sdk_key = zoom_conf["zoom_sdk_key"]
    payload_dict = {
        "sdkKey": zoom_sdk_key,
        "mn": data["meeting_id"],
        "role": data["role"],
        "iat": iat,
        "exp": exp,
        "appKey": zoom_sdk_key,
        "tokenExp": iat + 60 * 60 * 2,
    }
    zoom_secret_key = zoom_conf["zoom_secret_key"]
    return jwt.encode(
        payload=payload_dict,
        headers=header_dict,
        key=zoom_secret_key,
        algorithm="HS256",
    )


class GenerateSignatureAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GenerateSignatureSerializer

    def post(self, request):
        serializer = GenerateSignatureSerializer(data=request.data)
        if serializer.is_valid():
            signature = generate_signature(serializer.data)
            print(signature)
            return Response({"signature": signature})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
