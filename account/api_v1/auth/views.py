from datetime import datetime, timezone
from uuid import uuid4

import jwt
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.bl.exceptions import AccountDisableError, InvalidCredentialsError
from account.bl.registration import authenticate_user
from account.models.tokens import BlackListedToken
from account.models.users import User

from .serializers import LoginSerializer, RefreshSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Вход в систему",
        description="Получение пары JWT токенов по email и паролю.",
        request=LoginSerializer,
        auth=None,
        tags=["auth"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        try:
            user = authenticate_user(email, password)
        except InvalidCredentialsError:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        except AccountDisableError:
            return Response({"detail": "Аккаунт отключен"}, status=status.HTTP_403_FORBIDDEN)

        now = datetime.now(timezone.utc)
        access_token = jwt.encode(
            {
                "sub": str(user.pk),
                "iat": now,
                "exp": now + settings.JWT_ACCESS_TOKEN_LIFETIME,
                "type": "access",
                "jti": uuid4().hex,
            },
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM,
        )
        refresh_token = jwt.encode(
            {
                "sub": str(user.pk),
                "iat": now,
                "exp": now + settings.JWT_REFRESH_TOKEN_LIFETIME,
                "type": "refresh",
                "jti": uuid4().hex,
            },
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM,
        )
        return Response({"access": access_token, "refresh": refresh_token})


class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Обновить токены",
        description="Обмен refresh токена на новую пару access+refresh.",
        request=RefreshSerializer,
        auth=None,
        tags=["auth"],
    )
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.ExpiredSignatureError:
            return Response({"detail": "Refresh token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        if payload.get("type") != "refresh":
            return Response({"detail": "Not a refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        jti = payload["jti"]
        if BlackListedToken.objects.filter(jti=jti).exists():
            return Response({"detail": "Token revoked"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(pk=payload["sub"])
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active or not user.is_verified:
            return Response({"detail": "User inactive or not verified"}, status=status.HTTP_403_FORBIDDEN)

        now = datetime.now(timezone.utc)
        new_access = jwt.encode(
            {
                "sub": str(user.pk),
                "iat": now,
                "exp": now + settings.JWT_ACCESS_TOKEN_LIFETIME,
                "type": "access",
                "jti": uuid4().hex,
            },
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM,
        )
        new_refresh = jwt.encode(
            {
                "sub": str(user.pk),
                "iat": now,
                "exp": now + settings.JWT_REFRESH_TOKEN_LIFETIME,
                "type": "refresh",
                "jti": uuid4().hex,
            },
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM,
        )
        BlackListedToken.objects.create(
            jti=jti, expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc), user=user
        )
        return Response({"access": new_access, "refresh": new_refresh})


class LogoutView(APIView):
    @extend_schema(
        summary="Выход",
        description="Добавляет текущий access токен в чёрный список. Требуется заголовок Authorization: Bearer <token>.",
        tags=["auth"],
    )
    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"detail": "Authorization header required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return Response({"detail": "Bearer token required"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"detail": "Invalid Authorization header"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        except jwt.InvalidTokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        jti = payload.get("jti")
        if not jti:
            return Response({"detail": "Token missing jti"}, status=status.HTTP_400_BAD_REQUEST)
        if BlackListedToken.objects.filter(jti=jti).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        BlackListedToken.objects.create(
            jti=jti,
            expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            user=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
