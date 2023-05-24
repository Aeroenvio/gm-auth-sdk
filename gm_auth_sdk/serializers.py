from rest_framework.serializers import CurrentUserDefault as RestCurrentUserDefault

from .models import TokenUser


class CurrentUserDefault(RestCurrentUserDefault):
    requires_context = True

    def __call__(self, serializer_field) -> TokenUser:
        user: TokenUser = serializer_field.context["request"].user
        return user


class CurrentUserDefaultID(CurrentUserDefault):
    requires_context = True

    def __call__(self, serializer_field):
        user = super().__call__(serializer_field)
        return user.id
