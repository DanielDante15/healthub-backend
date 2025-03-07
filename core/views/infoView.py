from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import *
from ..serializers.infoSerializer import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    if request.method == 'POST':
        serializer = SpecialistInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Item created successfully.',
                'item': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_items(request):
    if request.method == 'GET':
        items = SpecialistInfo.objects.all()
        serializer = SpecialistInfoSerializer(items, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_item(request, item_id):
    try:
        item = SpecialistInfo.objects.get(id=item_id)
    except SpecialistInfo.DoesNotExist:
        return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpecialistInfoSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpecialistInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = SpecialistInfoSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response({"detail": "Specialist info deleted successfully"}, status=status.HTTP_204_NO_CONTENT)