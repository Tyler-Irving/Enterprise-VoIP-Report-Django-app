from rest_framework import serializers
from .models import ServiceLocationModel, NumberStatusModel

class ServiceLocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ServiceLocationModel
        fields = (
            'id', 'service_location_value', 'service_location_description'
        )

class NumberStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = NumberStatusModel
        fields = (
            'id', 'value', 'description'
        )