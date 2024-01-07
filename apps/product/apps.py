from django.apps import AppConfig


class ProductConfig(AppConfig):
    """
    Configuration for the 'product' application in Django.

    This class represents the specific configuration for the 'product' application.

    Attributes:
    - default_auto_field (str): Specifies the type of automatic field to be used
                              for models in this application.
    - name (str): The name of the application ('apps.product').
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.product"
