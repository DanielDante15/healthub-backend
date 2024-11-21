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
    class UserSummarySerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['name', 'email']  

    user_common = UserSummarySerializer()
    user_specialist = UserSummarySerializer()

    class Meta:
        model = Appointment
        fields = [
            'id', 'user_common', 'user_specialist', 'date_time', 
            'duration', 'address_or_link', 'is_online', 'status'
        ]

    
