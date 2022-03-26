from rest_framework import serializers

from testcases.serializers import I_P_Serializer
from configures.models import Configures


# 直接导入I_P_Serializer类，复用代码
class ConfigSerializer(serializers.ModelSerializer):
    interface = I_P_Serializer(label='配置所属接口名称，项目名称',
                               help_text='配置所属接口名称，项目名称')

    class Meta:
        model = Configures
        fields = ('id', 'name', 'interface', 'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            },
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['interface_id'] = result.pop('interface').get('iid')
        return result
