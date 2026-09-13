import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from account.bl.exceptions import (
    AccountDisableError,
    InvalidCredentialsError,
    RateLimitError,
    UniqueEmailError,
    UniquePhoneError,
)
from account.models.codes import EmailConfirmationCode
from account.models.users import User


def hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def register_user(data: dict) -> User:
    with transaction.atomic():
        try:
            user = User(
                email=data["email"],
                role=data["role"],
                phone=data["phone"],
                is_verified=False,
                is_active=True,
            )
            user.set_password(data["password"])
            user.save()
        except IntegrityError as e:
            msg = str(e).lower()
            if "email" in msg:
                raise UniqueEmailError()
            if "phone" in msg:
                raise UniquePhoneError()
            raise
        code = create_verification_code(user=user)
        send_verification_email(email=user.email, code=code)
    return user


def email_code_generator(length: int = 6) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(length))


def create_verification_code(user: User) -> str:
    code = email_code_generator()
    EmailConfirmationCode.objects.create(
        user=user,
        code_hash=hash_code(code),
        expires_at=timezone.now() + timedelta(minutes=10),
    )
    return code


def send_verification_email(email: str, code: str) -> None:
    subject = "Подтверждение регистрации"
    message = f"Ваш код подтверждения: {code}\nКод действителен 10 минут."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def verify_code(email: str, code: str) -> User:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError("Пользователь не найден")
    verification_code = EmailConfirmationCode.objects.filter(
        user=user,
        code_hash=hash_code(code),
        is_used=False,
        expires_at__gt=timezone.now(),
    ).first()
    if not verification_code:
        raise ValidationError("Неверный или истекший код")
    with transaction.atomic():
        user.is_verified = True
        user.save()
        verification_code.is_used = True
        verification_code.save()
        EmailConfirmationCode.objects.filter(user=user, is_used=False).exclude(pk=verification_code.pk).update(
            is_used=True
        )
    return user


def authenticate_user(email: str, password: str) -> User:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise InvalidCredentialsError()
    if not user.check_password(password):
        raise InvalidCredentialsError()
    if not user.is_active or not user.is_verified:
        raise AccountDisableError()
    return user


def resend_confirmation_code(email: str) -> None:
    try:
        user = User.objects.get(email=email, is_verified=False)
    except User.DoesNotExist:
        raise ValidationError("Пользователь не найден или уже подтверждён")
    codes_count = EmailConfirmationCode.objects.filter(
        user=user,
        created_at__gte=timezone.now() - timedelta(hours=1),
    ).count()
    if codes_count >= 3:
        raise RateLimitError()
    with transaction.atomic():
        EmailConfirmationCode.objects.filter(user=user, is_used=False).update(is_used=True)
        code = create_verification_code(user)
    send_verification_email(email, code)
