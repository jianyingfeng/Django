from rest_framework import serializers
from utils.validator import IsIdExists


class RunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='接口关联的环境配置id', help_text='接口关联的环境配置id',
                                      validators=[IsIdExists('env')])

    class Meta:
        model = object
        fields = ('id', 'env_id')
        extra_kwargs = {
            'env_id': {
                'write_only': True
            }
        }