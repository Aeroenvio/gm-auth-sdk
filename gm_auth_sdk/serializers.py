from rest_framework.serializers import CurrentUserDefault as RestCurrentUserDefault

from .models import TokenUser
from .client import GMAuthClient

class CurrentUserDefault(RestCurrentUserDefault):
    requires_context = True

    def __call__(self, serializer_field) -> TokenUser:
        request = serializer_field.context["request"]
        client = GMAuthClient()
        return client.get_current_user(request)
    

class CurrentUserDefaultID(CurrentUserDefault):
    requires_context = True

    def __call__(self, serializer_field):
        user = super().__call__(serializer_field)
        return user.id
