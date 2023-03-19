import json

from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.conf import settings
from django.contrib.auth.middleware import get_user
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


class MoveJWTCookieIntoTheBody(MiddlewareMixin):
    """for Django Rest Framework JWT's POST "/dj-rest-auth/token/verify/" endpoint.

    check for a 'token' in the request.COOKIE and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == reverse_lazy("token_verify"):
            if settings.JWT_AUTH_COOKIE in request.COOKIES:
                data = json.loads(request.body)
                data["token"] = request.COOKIES[settings.JWT_AUTH_COOKIE]
                request._body = json.dumps(data).encode("utf-8")
            elif settings.REST_USE_JWT:
                return HttpResponse("Permission Denied", status=401)
        return None


class OneJWTPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path == reverse_lazy("auth_refresh")
            and request.user.is_authenticated
        ):
            request.past_user = request.user
            tokens = cache.get(f"{request.user.id}-token")
            refresh_token = request.COOKIES.get(settings.JWT_AUTH_REFRESH_COOKIE, None)
            if tokens and refresh_token and (refresh_token != tokens["refresh"]):
                response = HttpResponse("Permission Denied", status=401)
                response.delete_cookie(settings.JWT_AUTH_COOKIE)
                response.delete_cookie(settings.JWT_AUTH_REFRESH_COOKIE)
                return response

        if request.path == reverse_lazy("auth_login"):
            return self.get_response(request)

        if request.user.is_authenticated:
            tokens = cache.get(f"{request.user.id}-token")
            access_token = request.COOKIES.get(settings.JWT_AUTH_COOKIE, None)
            refresh_token = request.COOKIES.get(settings.JWT_AUTH_REFRESH_COOKIE, None)
            if tokens and access_token and (access_token != tokens["access"]):
                response = HttpResponse("Permission Denied", status=401)
                response.delete_cookie(settings.JWT_AUTH_COOKIE)
                response.delete_cookie(settings.JWT_AUTH_REFRESH_COOKIE)
                return response
        return self.get_response(request)


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JWTCookieAuthentication()
        if jwt_data := jwt_authentication.authenticate(request):
            return jwt_data[0]
        return user
