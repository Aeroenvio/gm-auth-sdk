from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gm_auth_sdk.models import TokenUser


@api_view(["GET"])
def test_view(request):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({"message": "Hello, World!"})


@api_view(["GET"])
def test_user(request):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    user: TokenUser = request.user
    data = {"id": user.id, "pk": user.pk, "name": user.name}

    return Response(data)
