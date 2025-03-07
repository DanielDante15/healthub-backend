from rest_framework import serializers
from ..models import * 


class SpecialistInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistInfo
        fields ="__all__"