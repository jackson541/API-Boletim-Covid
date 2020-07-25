from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone
from django.conf import settings


#Retorna a diferença entre o tempo de expiração e o tempo passado
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

#Retorna se o tempo para expirar já terminou
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

#Verifica se o token já expirou, se sim, o deleta e cria um novo
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key = key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token inválido")

        if not token.user.is_active:
            raise AuthenticationFailed("User não está ativo")

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("Esse Token expirou")

        return (token.user, token)