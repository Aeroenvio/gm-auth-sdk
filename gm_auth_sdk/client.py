from dataclasses import asdict
from typing import Optional

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .authentication import BearerAuth
from .models import Agency


class GMAuthClient:
    def __init__(self, credentials: Optional[dict] = None) -> None:
        if "GM_AUTH_API_URL" not in settings:
            raise ImproperlyConfigured(
                "GM_AUTH_API_URL must be set in settings in order "
                "to connect with Grandmercado Authentication API"
            )

        self.auth_api = settings.get("GM_AUTH_API_URL")

        if credentials is None:
            if "GM_AUTH_CREDENTIALS" not in settings:
                raise ImproperlyConfigured(
                    "GM_AUTH_CREDENTIALS must be set in settings in order "
                    "to connect with Grandmercado Authentication API"
                )

            credentials = settings.get("GM_AUTH_CREDENTIALS")

        self.access_token = self._get_access_token(credentials)
        self.session = requests.session()
        self.session.auth = BearerAuth(token=self.access_token)

    # def list_agencies(self):
    #     response = self.session.get(f"{self.auth_api}/admin/agencies/")

    #     if response.status_code != 200:
    #         raise Exception(response.text)

    #     data = response.json()

    def create_agency(self, agency: Agency):
        url = f"{self.auth_api}/admin/agencies/"
        response = self.session.post(url, json=asdict(agency))

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    def update_agency(self, agency: Agency):
        url = f"{self.auth_api}/admin/agencies/{agency.id}/"
        response = self.session.put(url, json=asdict(agency))

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    def _get_access_token(self, credentials: dict) -> str:
        response = requests.post(
            f"{self.auth_api}/accounts/login/",
            data=credentials,
        )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()["access"]
