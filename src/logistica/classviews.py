from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Producer
from .serializers import ProducerSerializer


class ProducerLC(generics.ListCreateAPIView):
    """
    Listar y crear Producers
    """
    serializer_class = ProducerSerializer
    # TODO: implementar permisos?
    permission_classes = (AllowAny, )
    queryset = Producer.objects.all()


class ProducerRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    # TODO: implementar permisos?
    permission_classes = (AllowAny, )
