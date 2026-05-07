from rest_framework.exceptions import APIException


class GameNotFound(APIException):
    status_code = 404
    default_detail = "Игра не найдена"


class NotAnOrganizer(APIException):
    status_code = 403
    default_detail = "Пользователь не является организатором"


class NotAPlayer(APIException):
    status_code = 403
    default_detail = "Пользователь не является игроком"


class GameRegistrationClosed(APIException):
    status_code = 400
    default_detail = "Запись на игру закрыта"


class GameFull(APIException):
    status_code = 409
    default_detail = "Все места заняты"


class AlreadyRegistered(APIException):
    status_code = 409
    default_detail = "Вы уже записаны на эту игру"


class RegistrationNotFound(APIException):
    status_code = 404
    default_detail = "Запись не найдена"


class PaymentAlreadyExists(APIException):
    status_code = 409
    default_detail = "Платёж уже создан"


class PaymentError(APIException):
    status_code = 400
    default_detail = "Ошибка платежа"
