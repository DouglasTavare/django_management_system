from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Field 'name' must have at least 3 characters")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Field 'description' must have at least 10 characters")
        return value
    
    def validate_price(self, value):
        if value < 500:
            raise serializers.ValidationError("Field 'price' must be higher than 500")
        return value