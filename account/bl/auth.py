import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

from account.models.tokens import BlackListedToken

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return None
        except ValueError:
            raise exceptions.AuthenticationFailed("Invalid token header")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        jti = payload.get("jti")
        if jti and BlackListedToken.objects.filter(jti=jti).exists():
            raise exceptions.AuthenticationFailed("Token revoked")

        try:
            user = User.objects.get(pk=payload["sub"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
        if not user.is_active or not user.is_verified:
            raise exceptions.AuthenticationFailed("User inactive or not verified")

        return (user, payload)
