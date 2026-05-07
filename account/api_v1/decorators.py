from functools import wraps

from django.core.exceptions import PermissionDenied


def require_rolse(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
                roles
                if request.user.role not in roles:
                    raise PermissionDenied(f"Требуется роль: {roles}")
                return func(self, request, *args, **kwargs)
        return wrapper
    return decorator