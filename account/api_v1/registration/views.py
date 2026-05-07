from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.bl.exceptions import RateLimitError, UniqueEmailError
from account.bl.registration import register_user, resend_confirmation_code, verify_code

from .serializers import ResendCodeSerializer, UserCreateSerializer, VerifyEmailSerializer


class UserCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя и отправляет код подтверждения на email.",
        request=UserCreateSerializer,
        tags=["registration"],
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register_user(serializer.validated_data)
        except UniqueEmailError:
            return Response({"detail": "Email уже зарегистрирован"}, status=status.HTTP_409_CONFLICT)
        return Response(
            {
                "id": str(user.pk),
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Подтверждение email",
        description="Проверяет код и активирует аккаунт.",
        request=VerifyEmailSerializer,
        tags=["registration"],
    )
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            verify_code(serializer.validated_data["email"], serializer.validated_data["code"])
        except ValidationError:
            return Response({"detail": "Неверный или истекший код"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Аккаунт успешно активирован"})


class ResendCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Повторный код",
        description="Отправляет новый код подтверждения (не более 3 раз в час).",
        request=ResendCodeSerializer,
        tags=["registration"],
    )
    def post(self, request):
        serializer = ResendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            resend_confirmation_code(serializer.validated_data["email"])
        except RateLimitError:
            return Response({"detail": "Слишком много запросов"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        return Response({"detail": "Код повторно отправлен"})
