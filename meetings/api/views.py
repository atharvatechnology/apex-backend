from time import time

import jwt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import GenerateSignatureSerializer


def generate_signature(data):
    iat = round(time()) - 30
    exp = iat + 60 * 60 * 2
    header_dict = {"alg": "HS256", "typ": "JWT"}
    zoom_sdk_key = "1Pdmz2ex00PWc2Pj9F1Fb0hzH4sq8SmuFZVm"
    payload_dict = {
        "sdkKey": zoom_sdk_key,
        "mn": data["meeting_id"],
        "role": data["role"],
        "iat": iat,
        "exp": exp,
        "appKey": zoom_sdk_key,
        "tokenExp": iat + 60 * 60 * 2,
    }
    zoom_secret_key = "3EWQHADjLwHeHWOG8E0V85nXRlbgJ032dTNV"
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
