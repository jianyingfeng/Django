from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator
from utils.pagination import PageNumberPagination

from apps.debugtalks.models import DebugTalks


class DebugTalksModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebugTalks
        fields = '__all__'