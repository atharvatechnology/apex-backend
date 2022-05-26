import json

from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MoveJWTCookieIntoTheBody(MiddlewareMixin):
    """for Django Rest Framework JWT's POST "/dj-rest-auth/token/verify/" endpoint.

    check for a 'token' in the request.COOKIE and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == "/auth/token/verify/":
            if settings.JWT_AUTH_COOKIE in request.COOKIES:
                data = json.loads(request.body)
                data["token"] = request.COOKIES[settings.JWT_AUTH_COOKIE]
                request._body = json.dumps(data).encode("utf-8")
            elif settings.REST_USE_JWT:
                return HttpResponse("Permission Denied", status=401)
        return None
