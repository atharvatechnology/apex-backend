import hmac
import logging
from time import time

import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from enrollments.models import CourseThroughEnrollment, SessionStatus
from meetings.api_admin.serializers import MeetingSerializer
from meetings.models import Meeting

from .serializers import GenerateSignatureSerializer

logger = logging.getLogger(__name__)


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
            # print(signature)
            return Response({"signature": signature})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeetingListView(ListAPIView):
    queryset = Meeting.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if enrollment := CourseThroughEnrollment.objects.filter(
                enrollment__student=self.request.user,
                selected_session__status=SessionStatus.ACTIVE,
            ):
                meeting = Meeting.objects.none()
                for enroll in enrollment:
                    session = enroll.selected_session
                    meeting_session = Meeting.objects.filter(course_session=session)
                    meeting = meeting | meeting_session
                return meeting
        return None


@csrf_exempt
@api_view(["POST"])
def zoom_webhook(request):
    # get zoom token
    zoom_token = settings.ZOOM_CONFIGS["zoom_webhook_token"]

    # get webhook headers
    webhook_headers = request.headers
    zoom_signature = webhook_headers.get("x-zm-signature", "")

    # verify signature
    if zoom_signature:
        zoom_msg = (
            f"v0:{webhook_headers['x-zm-request-timestamp']}"
            + f":{request.body.decode('utf-8')}"
        )
        # get sha-256 encrypted token
        encrypted_token = hmac.new(
            key=zoom_token.encode("utf-8"),
            msg=zoom_msg.encode("utf-8"),
            digestmod="sha256",
        ).hexdigest()
        generated_signature = f"v0={encrypted_token}"
        # compare generated signature with webhook signature
        if generated_signature != zoom_signature:
            return Response(
                {"message": "Invalid Signature"}, status=status.HTTP_403_FORBIDDEN
            )

    # get webhook data
    webhook_data = request.data

    event_type = webhook_data.get("event", "endpoint.url_validation")
    resp_data = {}  # default response data
    if event_type == "endpoint.url_validation":
        # get plain token from request
        plain_token = webhook_data["payload"]["plainToken"]
        # use zoom token as salt to generate sha-256 encrypted token
        encrypted_token = hmac.new(
            key=zoom_token.encode("utf-8"),
            msg=plain_token.encode("utf-8"),
            digestmod="sha256",
        ).hexdigest()
        resp_data = {
            "plainToken": plain_token,
            "encryptedToken": encrypted_token,
        }
    elif event_type == "meeting.started":
        meeting_data = webhook_data["payload"]["object"]
        meeting_id = meeting_data["id"]
        try:
            meeting = Meeting.objects.get(meeting_id=meeting_id)
            meeting.start_meeting()
        except Meeting.DoesNotExist:
            logger.warning(f"Meeting with id {meeting_id} not found")

    elif event_type == "meeting.ended":
        meeting_data = webhook_data["payload"]["object"]
        meeting_id = meeting_data["id"]
        try:
            meeting = Meeting.objects.get(meeting_id=meeting_id)
            meeting.end_meeting()
        except Meeting.DoesNotExist:
            logger.warning(f"Meeting with id {meeting_id} not found")

    return Response(resp_data, status=status.HTTP_200_OK)
