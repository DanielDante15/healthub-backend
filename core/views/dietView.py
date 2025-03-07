from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import *
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError

from ..serializers.dietSerializer import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_diet(request):
    if request.method == 'POST':
        serializer = DietPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Diet created successfully.',
                'diet': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_diets(request):
    if request.method == 'GET':
        diets = DietPlan.objects.all()
        serializer = DietPlanSerializer(diets, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_diet(request, diet_id):
    try:
        diet = DietPlan.objects.get(id=diet_id)
    except DietPlan.DoesNotExist:
        return Response({"detail": "Diet not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DietPlanSerializer(diet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DietPlanSerializer(diet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = DietPlanSerializer(diet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        diet.delete()
        return Response({"detail": "Diet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
class DietPlanByUserEmailView(ReadOnlyModelViewSet):
    permission_classes = []
    serializer_class = DietPlanSerializer

    def get_queryset(self):
        user_email = self.request.query_params.get('user_email')
        if not user_email:
            raise ValidationError({"detail": "O parâmetro 'user_email' é obrigatório."})

        return DietPlan.objects.filter(
            models.Q(user__email=user_email) 
        )