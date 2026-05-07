from rest_framework.exceptions import APIException


class UniqueEmailError(APIException):
    status_code = 409
    default_detail = "Email должен быть уникальным"


class InvalidCredentialsError(APIException):
    status_code = 401
    default_detail = "Неверные учетные данные"


class AccountDisableError(APIException):
    status_code = 403
    default_detail = "Аккаунт отключен или не верифицирован"


class RateLimitError(APIException):
    status_code = 429
    default_detail = "Слишком много попыток, попробуйте позже"


class ProfileNotFound(APIException):
    status_code = 404
    default_detail = "Профиль не найден"


class ProfileAlreadyExists(APIException):
    status_code = 409
    default_detail = "Профиль уже существует"
