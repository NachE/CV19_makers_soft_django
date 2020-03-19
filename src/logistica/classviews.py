from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Production
from .serializers import ProductionSerializer


class ProductionLC(generics.ListCreateAPIView):
    """
    Listar y crear productions
    """
    serializer_class = ProductionSerializer
    # TODO: implementar permisos?
    permission_classes = (AllowAny, )
    queryset = Production.objects.all()


class ProductionRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    # TODO: implementar permisos?
    permission_classes = (AllowAny, )
