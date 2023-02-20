from django.conf import settings
from django.utils.translation import gettext_lazy as _
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

        return api_settings.TOKEN_USER_CLASS(validated_token)
