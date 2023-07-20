from django.apps import AppConfig


class CrudAppMasterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.crud_app_master"
    verbose_name="Master Data"
