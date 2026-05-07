import jwt as pyjwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import InvalidTokenError

from account.models.tokens import BlackListedToken

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        jti = payload.get("jti")
        if jti and BlackListedToken.objects.filter(jti=jti).exists():
            return None
        return User.objects.get(pk=payload["sub"])
    except (InvalidTokenError, User.DoesNotExist):
        return None


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = dict(p.split("=") for p in query_string.split("&") if "=" in p)
        token = params.get("token")
        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = None
        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)
