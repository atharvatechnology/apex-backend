import json

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware:
    """to set WWW-Authenticate = To none ---  This might not be required."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["WWW-Authenticate"] = None
        return response


class MoveJWTCookieIntoTheBody(MiddlewareMixin):
    """for Django Rest Framework JWT's POST "/dj-rest-auth/token/verify/" endpoint.

    check for a 'token' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if (
            request.path == "/dj-rest-auth/token/verify/"
            and settings.JWT_AUTH_COOKIE in request.COOKIES
            and request.body != b""
        ):
            data = json.loads(request.body)
            data["token"] = request.COOKIES[settings.JWT_AUTH_COOKIE]
            request._body = json.dumps(data).encode("utf-8")
        return None
