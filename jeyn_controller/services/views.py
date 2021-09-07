from rest_framework import viewsets

from . import models, serializers


class ServiceViewset(viewsets.ModelViewSet):

    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class ServiceVerionViewset(viewsets.ModelViewSet):
    queryset = models.ServiceVersion.objects.all()
    serializer_class = serializers.ServiceVerswionSerializer
