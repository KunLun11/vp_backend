from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Информация о себе",
        description="Возвращает данные текущего аутентифицированного пользователя.",
        tags=["users"],
    )
    def get(self, request):
        user = request.user
        return Response(
            {
                "id": str(user.pk),
                "email": user.email,
                "phone": str(user.phone),
                "role": user.role,
            }
        )
