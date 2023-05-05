from dataclasses import asdict, fields
from typing import Optional

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import ValidationError

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

    def create_agency(self, agency: Agency) -> Agency:
        url = f"{self.auth_api}/admin/accounts/agency/"

        files = {}
        if agency.logo:
            files["logo"] = agency.logo
        if agency.logo_small:
            files["logo_small"] = agency.logo_small
        if agency.favicon:
            files["favicon"] = agency.favicon

        agency_data = asdict(agency)
        agency_data.pop("logo")
        agency_data.pop("logo_small")
        agency_data.pop("favicon")

        try:
            response = self.session.post(url, data=agency_data, files=files)
            response.raise_for_status()
            # TODO: handle errors, just printing and re-raising for now
        except requests.exceptions.HTTPError as errh:
            if response.status_code == 400:
                raise ValidationError(response.json())
            raise errh
        except requests.exceptions.ConnectionError as errc:
            raise errc
        except requests.exceptions.Timeout as errt:
            raise errt
        except requests.exceptions.RequestException as err:
            raise err

        response_data = response.json()
        response_data = {
            k: v
            for k, v in response_data.items()
            if k in tuple(e.name for e in fields(Agency).keys())
        }

        return Agency(**response_data)

    def update_agency(self, partial_agency):
        url = f"{self.auth_api}/admin/accounts/agency/{partial_agency['app_id']}/"
        response = self.session.put(url, json=partial_agency)

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
