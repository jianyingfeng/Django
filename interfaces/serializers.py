from rest_framework import serializers


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