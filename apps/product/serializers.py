from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer is used to convert Product model instances to JSON and validate
    incoming data during deserialization.

    Attributes:
    - Meta (class): A inner class specifying metadata for the serializer.
        - model (class): The model class that the serializer is based on (Product).
        - fields (str or tuple): Specifies the fields to include in the serialized output.
                                 In this case, "__all__" includes all fields.

    Methods:
    - validate_name(self, value): Custom validation for the 'name' field.
                                  Raises a ValidationError if the length is less than 3.

    - validate_description(self, value): Custom validation for the 'description' field.
                                         Raises a ValidationError if the length is less than 10.

    - validate_price(self, value): Custom validation for the 'price' field.
                                   Raises a ValidationError if the value is less than 500.
    """
    class Meta:
        model = Product
        fields = "__all__"

    def validate_name(self, value):
        """
        Validate the 'name' field.

        Args:
        - value (str): The value of the 'name' field.

        Raises:
        - serializers.ValidationError: If the length of 'name' is less than 3.
        """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Field 'name' must have at least 3 characters"
            )

        return value

    def validate_description(self, value):
        """
        Validate the 'description' field.

        Args:
        - value (str): The value of the 'description' field.

        Raises:
        - serializers.ValidationError: If the length of 'description' is less than 10.
        """
        if len(value) < 10:
            raise serializers.ValidationError(
                "Field 'description' must have at least 10 characters"
            )

        return value

    def validate_price(self, value):
        """
        Validate the 'price' field.

        Args:
        - value (float): The value of the 'price' field.

        Raises:
        - serializers.ValidationError: If the 'price' is less than 500.
        """
        if value < 500:
            raise serializers.ValidationError(
                "Field 'price' must be higher than 500")

        return value
