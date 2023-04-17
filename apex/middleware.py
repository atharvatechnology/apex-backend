import contextlib
import json
import logging

from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.conf import settings
from django.contrib.auth.middleware import get_user
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from common.errors import StateTransitionError

logger = logging.getLogger(__name__)


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


def delete_cookies(response):
    """Delete JWT authentication cookies from an HTTP response.

    Args:
        response (HttpResponse): The response to modify.

    Returns
        HttpResponse: The modified HTTP response object.

    """
    response.delete_cookie(settings.JWT_AUTH_COOKIE)
    response.delete_cookie(settings.JWT_AUTH_REFRESH_COOKIE)
    return response


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
                return delete_cookies(response)

        if request.path == reverse_lazy("auth_login"):
            return self.get_response(request)

        if request.user.is_authenticated:
            tokens = cache.get(f"{request.user.id}-token")
            access_token = request.COOKIES.get(settings.JWT_AUTH_COOKIE, None)
            refresh_token = request.COOKIES.get(settings.JWT_AUTH_REFRESH_COOKIE, None)
            if tokens and access_token and (access_token != tokens["access"]):
                response = HttpResponse("Permission Denied", status=401)
                return delete_cookies(response)
        response = self.get_response(request)
        # remove dangling cookies if user is not authenticated
        return delete_cookies(response) if request.user.is_anonymous else response


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
        with contextlib.suppress(AuthenticationFailed):
            if jwt_data := jwt_authentication.authenticate(request):
                return jwt_data[0]
        return user


class ErrorHandlerMiddleware:
    """Handles known errors gracefully and returns a JSON response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ConnectionError):
            error_msg = exception.args[0] if exception.args else "Error in server"
            logger.exception(exception)
            return JsonResponse(
                {"error": "ConnectionError", "message": error_msg}, status=500
            )
        if isinstance(exception, StateTransitionError):
            error_msg = (
                exception.args[0] if exception.args else "Error in state handler"
            )
            logger.exception(exception)
            return JsonResponse(
                {"error": "StateTransitionError", "message": error_msg}, status=500
            )
