
"""View module for handling requests about game """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from music_repairsapi.models import Instrument


class InstrumentView(ViewSet):

    def list(self, request):
        instruments = Instrument.objects.all()
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        instrument = Instrument.objects.get(pk=pk)
        serializer = InstrumentSerializer(
            instrument, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstrumentSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer 
    """
    class Meta:
        model = Instrument
        fields = ('id', 'instrument_name')
