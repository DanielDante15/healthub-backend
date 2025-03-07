from rest_framework import serializers
from ..models import * 

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
        
class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class AppointmentSerializer(serializers.ModelSerializer):
    user_common = serializers.CharField(source='user_common.email')
    user_specialist = serializers.CharField(source='user_specialist.email') 

    class Meta:
        model = Appointment
        fields = [
            'id', 'user_common', 'user_specialist', 'date_time', 
            'duration', 'address_or_link', 'is_online', 'status'
        ]
        
    def create(self, validated_data):
        specialist = validated_data.pop('specialist_email')
        validated_data['specialist'] = specialist
        return super().create(validated_data)
    
    
class AppointmentCreateSerializer(serializers.ModelSerializer):
    # Campos para leitura (GET)
    user_common = serializers.CharField(source='user_common.email', read_only=True)
    appointment_type = serializers.CharField(source='user_specialist.role', read_only=True)
    specialist_name = serializers.CharField(source='user_specialist.name', read_only=True)
    user_specialist = serializers.CharField(source='user_specialist.email', read_only=True)

    # Campos para escrita (POST)
    user_common_email = serializers.EmailField(write_only=True)
    user_specialist_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'user_common', 'user_specialist', 'user_common_email', 
            'user_specialist_email','specialist_name', 'date_time', 'duration','appointment_type', 
            'address_or_link', 'is_online', 'status'
        ]

    def validate(self, data):
        """
        Valida se os emails fornecidos correspondem a usuários existentes.
        """
        # Valida o email de `user_common`
        try:
            data['user_common'] = User.objects.get(email=data.pop('user_common_email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({'user_common_email': 'Usuário comum com este email não encontrado.'})

        # Valida o email de `user_specialist`
        try:
            data['user_specialist'] = User.objects.get(email=data.pop('user_specialist_email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({'user_specialist_email': 'Usuário especialista com este email não encontrado.'})

        return data

    def create(self, validated_data):
        """
        Cria um Appointment com os dados validados.
        """
        return Appointment.objects.create(**validated_data)