
"""View module for handling requests about game """
from django.http import HttpResponseServerError
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from music_repairsapi.models import Specialty


class SpecialtyView(ViewSet):
    permission_classes = [AllowAny, ]

    def list(self, request):
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        specialty = Specialty.objects.get(pk=pk)
        serializer = SpecialtySerializer(
            specialty, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialtySerializer(serializers.ModelSerializer):
    """JSON serializer for gamer 
    """
    class Meta:
        model = Specialty
        fields = ('id', 'specialty_name')
