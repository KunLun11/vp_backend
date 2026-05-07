from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
    verbose_name = "Аккаунт"

    def ready(self):
        import account.auth_extension  # noqa: F401
