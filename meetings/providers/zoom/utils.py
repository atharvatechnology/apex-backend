# from datetime import datetime, timedelta
import json

import requests
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import localtime, now, timedelta
from rest_framework import status


def list_meetings(json_data):
    print("inside list meet")

    url = "https://api.zoom.us/v2/users/me/meetings"
    payload = {}
    headers = {
        "Authorization": "Bearer " + json_data["access_token"],
        "content-type": "application/json",
    }
    try:
        res = requests.request("GET", url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        return HttpResponse("Error connecting to zoom").status_code(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    data = res.text
    json_data = json.loads(data)
    # print(json_data)
    # return JsonResponse(json_data)
    return json_data


def delete_meeting(json_data, meeting_id):
    print("inside delete meet")
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    payload = ""
    headers = {
        "Authorization": "Bearer " + json_data["access_token"],
        "content-type": "application/json",
    }
    try:
        res = requests.request("DELETE", url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        return HttpResponse("Error connecting to zoom").status_code(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    # data = res.read()
    res_status = res.status_code
    return {
        "status": res_status,
    }


def create_meeting(json_data):
    print("inside create meet")
    url = "https://api.zoom.us/v2/users/me/meetings"
    now_time = now()
    plus_5_min = now_time + timedelta(minutes=5)
    meeting_time = localtime(plus_5_min).strftime("%Y-%m-%dT%H:%M:%S")
    print(meeting_time)

    payload = json.dumps(
        {
            "agenda": "Demo Apex Class",
            "default_password": False,
            "duration": 60,
            "password": "123456",
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
            "topic": "Apex first class",
            "type": 2,
        }
    )
    headers = {
        "Authorization": "Bearer " + json_data["access_token"],
        "Content-Type": "application/json",
    }
    try:
        res = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        return HttpResponse("Error connecting to zoom").status_code(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    data = res.text
    json_data = json.loads(data)
    return json_data


def index(request):
    # conn = http.client.HTTPSConnection("zoom.us")
    url = (
        "https://zoom.us/oauth/token?grant_type=account_credentials"
        + "&account_id=9cR1iFnhQTGeirfFdqQD2w"
    )
    payload = {}
    key = "aV9VV25SSThTQmVDclAwYWd4YW9JZzpuc0o3dXlUZld0VjJtVE1CMXpJbUo1MFN0Z3Z0UzdBdw=="
    headers = {
        "Authorization": f"Basic {key}",
        "content-type": "application/json",
    }
    # conn.request(
    #     "POST",
    #     "/oauth/token?grant_type=account_credentials&account_id=9cR1iFnhQTGeirfFdqQD2w",
    #     payload,
    #     headers,
    # )
    # res = conn.getresponse()
    try:
        res = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        return HttpResponse("Error connecting to zoom").status_code(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    text_data = res.text
    decoded_data = text_data
    # decoded_data = data.decode("utf-8")
    json_data = json.loads(decoded_data)
    print(res.status_code)

    if res.status_code == 200:
        meeting_data = create_meeting(json_data)
        return JsonResponse(meeting_data)

    return HttpResponse("Hello, world. You're at the polls index.")
