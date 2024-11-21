from rest_framework import serializers
from .models import User, Appointment
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'age', 'height','role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
    
class AppointmentSerializer(serializers.ModelSerializer):
    user_common = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.COMMON))
    user_specialist = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role__in=[User.PERSONAL_TRAINER, User.NUTRITIONIST]))
    date_time = serializers.DateTimeField()
    duration = serializers.DurationField()

    class Meta:
        model = Appointment
        fields = ['id', 'user_common', 'user_specialist', 'date_time', 'duration']

    def create(self, validated_data):
        # Aqui, você pode incluir validações adicionais se necessário
        return Appointment.objects.create(**validated_data)

    
