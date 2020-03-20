from rest_framework import serializers
from .models import Producer


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = (
            'pk',
            'region',
            'name',
            'point',
            'production_capacity',
            'logistics_need',
        )
