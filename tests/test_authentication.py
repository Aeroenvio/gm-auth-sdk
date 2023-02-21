#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_gm-auth-sdk
------------

Tests for `gm-auth-sdk` authentication Backend.
"""
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from gm_auth_sdk.models import TokenUser


class TestTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user"] = user
        return token


class TestGm_auth_sdk(APITestCase):
    def setUp(self):
        pass

    def test_authentication(self):
        class User:
            def __init__(self, id, name):
                self.id = id
                self.name = name

        user = User(1, "Test User")
        token: RefreshToken = RefreshToken.for_user(user)
        token["user"] = user.__dict__
        access = token.access_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Hello, World!")

    def test_authentication_for_invalid_user(self):
        class User:
            def __init__(self, id, name):
                self.id = id
                self.name = name

        user = User(1, "Test User")
        token: RefreshToken = RefreshToken.for_user(user)
        # Token dont define user field
        access = token.access_token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("test")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_authentication_with_invalid_token(self):
        access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ1c2VyIjp7ImlkIjoxLCJuYW1lIjoiVGVzdCJ9fQ.nxGhzLp9Xbi-mN6OSO1SNiOYAQWjYlODuVNIj8E8fAA"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("test")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

        data = response.json()
        self.assertEqual(data["code"], "token_not_valid")

    def test_token_models_fields(self):
        data = {
            "id": 1,
            "name": "Test User",
            "email": "test@test.com",
            "phone": "+5555555",
            "agency": "Grandmercado",
            "is_staff": True,
        }
        user = TokenUser(data)

        self.assertEqual(user.pk, 1)
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(str(user), "test@test.com")
        self.assertEqual(user.phone, "+5555555")
        self.assertEqual(user.agency, "Grandmercado")
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user, user)

        class Object:
            pass

        dumb_object = Object()
        dumb_object.id = 2

        self.assertNotEqual(user, dumb_object)

        d = {}
        d[user] = 3

    def tearDown(self):
        pass
