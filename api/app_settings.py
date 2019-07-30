from django.conf import settings
from api.serializers.authentication_serializers import (
    TokenSerializer as DefaultTokenSerializer,
    LoginSerializer as DefaultLoginSerializer,
    )
from .utils import import_callable, default_create_token

create_token = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = import_callable(
    serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)


#PasswordResetSerializer as DefaultPasswordResetSerializer,
#PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
#PasswordChangeSerializer as DefaultPasswordChangeSerializer
