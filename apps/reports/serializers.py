from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator
from utils.pagination import PageNumberPagination

from reports.models import Reports


# 获取列表时不返回summary字段
# 获取详情时返回summary字段
class ReportsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        read_only_fields = ('name', 'result', 'count', 'success')
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'html': {
                'write_only': True
            },
            'summary': {
                'write_only': True
            }
        }

    # to_representation会在action方法之后执行，从而实现对响应数据的修改
    # 将result字段中的1或0转换为pass或fail
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['result'] = 'pass' if data['result'] else 'fail'
        return data

    # def to_internal_value(self, data):
    #     print(11)