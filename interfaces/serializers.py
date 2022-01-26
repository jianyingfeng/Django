from rest_framework import serializers
from .models import Interfaces


class ProjectsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    leader = serializers.CharField()


class InterfacesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()
    # projects = serializers.PrimaryKeyRelatedField(read_only=True)
    # projects = serializers.StringRelatedField()
    # projects = serializers.SlugRelatedField(slug_field='name', read_only=True)
    projects = ProjectsSerializer()


class InterfacesSerializer0125(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name')