from rest_framework import viewsets, mixins
from debugtalks.models import DebugTalks
from debugtalks.serializers import DebugTalksModelSerializer, DebugTalksModelSerializer_One


class DebugtalkViewSet(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksModelSerializer_One

    def get_serializer_class(self):
        if self.action == 'list':
            return DebugTalksModelSerializer
        else:
            return super().get_serializer_class()
