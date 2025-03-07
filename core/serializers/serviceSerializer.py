from rest_framework import serializers
from ..models import * 

class ServiceSerializer(serializers.ModelSerializer):
    specialist_email = serializers.EmailField(write_only=True)
    specialist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'specialist_email', 'specialist', 'title', 'description', 'duration', 'price', 'service_type']
        read_only_fields = ['id', 'specialist']

    def validate_specialist_email(self, value):
        try:
            specialist = User.objects.get(email=value)
            if specialist.role not in [User.PERSONAL_TRAINER, User.NUTRITIONIST]:
                raise serializers.ValidationError("The specialist must be a Personal Trainer or Nutritionist.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return specialist

    def create(self, validated_data):
        specialist = validated_data.pop('specialist_email')
        validated_data['specialist'] = specialist
        return super().create(validated_data)

    def get_specialist(self, obj):
        if obj.specialist:
            return obj.specialist.email 
        return None