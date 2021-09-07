from rest_framework import serializers

from . import models


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = [
            "id", "name", "deployed", "deployment_scheme"
        ]

class ServiceVerswionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceVersion
        fields = [
            "id", "model_id"
        ]
