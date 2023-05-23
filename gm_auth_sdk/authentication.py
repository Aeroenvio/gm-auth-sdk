from django.utils.translation import gettext_lazy as _
from requests.auth import AuthBase
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings


class GMAuthentication(JWTStatelessUserAuthentication):
    """Authentication backend that takes an access token
    issued by this app and returns the user property
    """

    def get_user(self, validated_token):
        """
        Returns a stateless user object which is backed by the given validated
        token.
        """

        if "user" not in validated_token:
            # The TokenUser class assumes tokens will have a recognizable user
            # identifier claim.
            raise InvalidToken(_("Token contained no recognizable user identification"))

        return api_settings.TOKEN_USER_CLASS(validated_token.get("user"))


class TokenAuth(AuthBase):
    """Attaches a token to the given request object."""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"Token {self.token}"
        return request


class BearerAuth(AuthBase):
    """Attaches a token to the given request object."""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class GMAuth(AuthBase):
    """Attaches a token to the given request object."""

    def __init__(self, token, agency):
        self.token = token
        self.agency = agency

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        request.headers["X-APP-ID"] = f"{self.agency}"
        return request
