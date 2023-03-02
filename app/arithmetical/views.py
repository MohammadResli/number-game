"""
Views for the ariths API.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    ArithmeticalConceptModel,
    NumberModel,
)

from arithmetical.serializers import (
    ListArithmeticalConceptSerializer,
    ListNumberSerializer,
    DetailArithmeticalConceptSerializer,
    DetailNumberSerializer,
)


@api_view(['GET'])
def get_all_arithmetical_concepts(request):
    "Get list of all arithmetical concepts in the game."
    ariths = ArithmeticalConceptModel.objects.all().order_by('id')
    serializer = ListArithmeticalConceptSerializer(ariths, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_numbers(request):
    "Get list of all numbers in the game."
    numbers = NumberModel.objects.all().order_by('value')
    serializer = ListNumberSerializer(numbers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_arithmetical_concept_detail(request, id):
    model = ArithmeticalConceptModel
    try:
        arith = model.objects.get(
            id=id,
        )
        serializer = DetailArithmeticalConceptSerializer(arith)
        return Response(serializer.data)
    except model.DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_number_detail(request, id):
    model = NumberModel
    try:
        number = model.objects.get(
            id=id,
        )
        serializer = DetailNumberSerializer(number)
        return Response(serializer.data)
    except model.DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
