import json
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status

from meetings.providers.base import BasicProvider


class ZoomProvider(BasicProvider):
    def __init__(self):
        config = settings.ZOOM_CONFIGS
        self.api_url = config["zoom_api"]
        self.account_id = config["zoom_account_id"]
        self.key = config["zoom_key"]
        self.retry_attempts = config["zoom_retry_attempts"]
        self.get_access_token()

    def get_access_token(self):
        url = (
            "https://zoom.us/oauth/token?grant_type=account_credentials"
            + f"&account_id={self.account_id}"
        )
        payload = {}
        headers = {
            "Authorization": f"Basic {self.key}",
            "content-type": "application/json",
        }

        try:
            res = requests.request("POST", url, headers=headers, data=payload)
            # print(res.text)
            if res.status_code != 200:
                raise ConnectionError("Error connecting to zoom")
        except Exception as e:
            # print(e)
            raise ConnectionError("Error connecting to zoom") from e

        data = res.text
        json_data = json.loads(data)
        self.access_token = json_data["access_token"]

    def send_request(self, request_type, url, headers, payload):
        try:
            res = requests.request(request_type, url, headers=headers, data=payload)
        except Exception:
            # print(e)
            return HttpResponse("Error connecting to zoom").status_code(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        data = res.text
        # print(res.status_code)
        # print(res.text)
        json_data = json.loads(data) if data else None
        # print(json_data)
        return res, json_data

    def attempt_zoom_connection(self, request_type, url, headers, payload):
        for _ in range(self.retry_attempts):
            res, json_data = self.send_request(request_type, url, headers, payload)
            # print(res, json_data)
            if res.status_code == 401 and json_data.get("code") == 124:
                self.get_access_token()
            elif res.status_code in [200, 201, 204]:
                return json_data
            elif res.status_code == 404 and json_data.get("code") == 3001:
                return json_data
        raise ConnectionError("Error connecting to zoom")

    def get_meetings(self):
        # print("inside list meet")
        url = urljoin(self.api_url, "users/me/meetings")
        payload = {}
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
        }
        return self.attempt_zoom_connection("GET", url, headers, payload)

    # def send_post_request(self, url, headers, payload):
    #     try:
    #         res = requests.request("POST", url, headers=headers, data=payload)
    #     except Exception as e:
    #         print(e)
    #         return HttpResponse("Error connecting to zoom").status_code(
    #             status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )
    #     data = res.text
    #     json_data = json.loads(data)
    #     return res, json_data

    def create_meeting(self, meeting_config):
        # print("inside create meet")
        url = urljoin(self.api_url, "users/me/meetings")
        meeting_time = meeting_config["start_time"]
        payload = json.dumps(
            {
                "agenda": meeting_config["title"],
                "default_password": False,
                "duration": meeting_config["duration"],
                "password": meeting_config["password"],
                "pre_schedule": False,
                "settings": {
                    "allow_multiple_devices": True,
                    "approval_type": 2,
                    "audio": "both",
                    "auto_recording": "cloud",
                    "calendar_type": 1,
                    "close_registration": False,
                    "email_notification": False,
                    "encryption_type": "enhanced_encryption",
                    "focus_mode": True,
                    "host_video": True,
                    "jbh_time": 0,
                    "join_before_host": False,
                    "meeting_authentication": False,
                    "mute_upon_entry": False,
                    "participant_video": False,
                    "private_meeting": False,
                    "use_pmi": False,
                    "waiting_room": False,
                    "watermark": True,
                    "host_save_video_order": False,
                    "alternative_host_update_polls": False,
                },
                "start_time": meeting_time,
                "template_id": "Dv4YdINdTk+Z5RToadh5ug==",
                "timezone": "Asia/Kathmandu",
                "topic": meeting_config["title"],
                "type": 8,
                "recurrence": {
                    "type": meeting_config["repeat_type"],
                    "end_date_time": meeting_config["end_date_time"],
                    "repeat_interval": meeting_config["repeat_interval"],
                    "monthly_day": meeting_config["monthly_day"],
                    "weekly_days": meeting_config["weekly_days"],
                },
            }
        )
        # print(payload)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
        }

        return self.attempt_zoom_connection("POST", url, headers, payload)

    def update_meetings(self, *args, **kwargs):
        raise NotImplementedError

    def delete_meeting(self, meeting_id):
        # print("inside delete meet")
        url = urljoin(self.api_url, f"meetings/{meeting_id}")
        payload = {}
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
        }

        return self.attempt_zoom_connection("DELETE", url, headers, payload)
