from rest_framework.exceptions import APIException


class ChatRoomNotFound(APIException):
    status_code = 404
    default_detail = "Чат-комната не найдена"


class ChatMemberNotFound(APIException):
    status_code = 404
    default_detail = "Участник чата не найден"


class UserMuted(APIException):
    status_code = 403
    default_detail = "Пользователь заглушен"
