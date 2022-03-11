from rest_framework import viewsets

from .serializers import EnvsSerializers
from .models import Envs


class EnvsViewSet(viewsets.ModelViewSet):
    serializer_class = EnvsSerializers
    queryset = Envs.objects.all()
