from rest_framework import serializers
from .models import Production


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = (
            'pk',
            'region',
            'name',
            'point',
            'production_capacity',
            'logistics_need',
        )
