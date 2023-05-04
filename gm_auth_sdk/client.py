from dataclasses import asdict
from typing import Optional

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .authentication import BearerAuth
from .models import Agency


class GMAuthClient:
    def __init__(self, credentials: Optional[dict] = None) -> None:
        if not hasattr(settings, "GM_AUTH_API_URL"):
            raise ImproperlyConfigured(
                "GM_AUTH_API_URL must be set in settings in order "
                "to connect with Grandmercado Authentication API"
            )

        self.auth_api = settings.GM_AUTH_API_URL

        if credentials is None:
            if not hasattr(settings, "GM_AUTH_CREDENTIALS"):
                raise ImproperlyConfigured(
                    "GM_AUTH_CREDENTIALS must be set in settings in order "
                    "to connect with Grandmercado Authentication API"
                )

            credentials = settings.GM_AUTH_CREDENTIALS

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

        files = {}

        with open(agency.logo, "rb") as logo_file:
            files["logo"] = logo_file
        with open(agency.logo_small, "rb") as logo_small_file:
            files["logo_small"] = logo_small_file
        with open(agency.favicon, "rb") as favicon_file:
            files["favicon"] = favicon_file

        response = self.session.post(url, data=asdict(agency), files=files)

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    def update_agency(self, partial_agency):
        url = f"{self.auth_api}/admin/agencies/{partial_agency['id']}/"
        response = self.session.put(url, json=partial_agency)

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    def _get_access_token(self, credentials: dict) -> str:
        print(credentials)
        response = requests.post(
            f"{self.auth_api}/accounts/login/",
            data=credentials,
            headers={"X-APP-ID": credentials.get("agency")},
        )
        print(response.request.headers)

        if response.status_code != 200:
            raise Exception(response.text)
        print(response.json())
        return response.json()["access_token"]
