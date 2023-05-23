from dataclasses import dataclass

from django.contrib.auth import models as auth_models
from django.db.models.manager import EmptyManager
from django.utils.functional import cached_property


class TokenUser:
    """
    A user class modeled for GM.
    Used in conjunction with the `GMAuthentication` backend to
    implement single sign-on functionality across services which share the same
    secret key.  `GMAuthentication` will return an instance of this
    class instead of a `User` model instance.  Instances of this class act as
    stateless user objects which are backed by validated tokens.
    """

    # User is always active since Simple JWT will never issue a token for an
    # inactive user
    is_active = True

    _groups = EmptyManager(auth_models.Group)
    _user_permissions = EmptyManager(auth_models.Permission)

    def __init__(self, user):
        self._user = user

    def __str__(self):
        return f"{self.email}"

    @cached_property
    def id(self):
        return self._user["id"]

    @cached_property
    def pk(self):
        return self.id

    @cached_property
    def name(self):
        return self._user.get("name", "")

    @cached_property
    def email(self):
        return self._user.get("email", "")

    @cached_property
    def agency(self):
        return self._user.get("agency", "")

    @cached_property
    def phone(self):
        return self._user.get("phone", "")

    @cached_property
    def is_staff(self):
        return self._user.get("is_staff", False)

    @cached_property
    def is_superuser(self):
        return self._user.get("is_superuser", False)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def save(self):
        raise NotImplementedError("Token users have no DB representation")

    def delete(self):
        raise NotImplementedError("Token users have no DB representation")

    def set_password(self, raw_password):
        raise NotImplementedError("Token users have no DB representation")

    def check_password(self, raw_password):
        raise NotImplementedError("Token users have no DB representation")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return False

    def has_module_perms(self, module):
        return False

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.email

    def __getattr__(self, attr):
        """This acts as a backup attribute getter for custom claims
        defined in Token serializers."""
        return self._user.get(attr, None)


@dataclass
class Agency:
    app_id: str
    name: str
    code: str
    domain: str
    primary_color: str
    logo: str
    logo_small: str
    favicon: str
    phone: str
    email: str
    address: str
    password: str


@dataclass
class User:
    id: str
    email: str
    name: str
    phone: str
    agency: str
    email_verified: bool = False
    phone_verified: bool = False
