from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError



from ..models import *
from ..serializers.appointmentSerializer import *

@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Autenticação necessária
def create_appointment(request):
    if request.method == 'POST':
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Appointment created successfully.',
                'appointment': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Listar todos os agendamentos
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Autenticação necessária
def list_appointments(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


# Detalhes de um agendamento específico
@api_view(['GET','PUT','PATCH','DELETE'])
# @permission_classes([IsAuthenticated])  # Autenticação necessária
def manage_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"detail": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    elif request.method == 'GET':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        appointment.delete()
        return Response({"detail": "Appointment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class AppointmentsByUserEmail(ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = AppointmentCreateSerializer

    def get_queryset(self):
        # Obtém o parâmetro 'user_email' da URL
        user_email = self.request.query_params.get('user_email')
        if not user_email:
            raise ValidationError({"detail": "O parâmetro 'user_email' é obrigatório."})

        # Verifica os appointments relacionados ao user_common ou user_specialist
        return Appointment.objects.filter(
            models.Q(user_common__email=user_email) | models.Q(user_specialist__email=user_email)
        )