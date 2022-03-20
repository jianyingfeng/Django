from rest_framework import viewsets

from testsuites.models import Testsuites
from testsuites.serializers import TestsuitesModelSerializer


class TestsuitesViewSet(viewsets.ModelViewSet):
    serializer_class = TestsuitesModelSerializer
    queryset = Testsuites.objects.all()
