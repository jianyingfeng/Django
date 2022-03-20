from rest_framework import serializers

from .models import Envs


class EnvsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Envs
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class EnvsNamesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Envs
        fields = ('id', 'name')
