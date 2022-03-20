from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import EnvsSerializers, EnvsNamesSerializers
from .models import Envs
from utils.mixins import NamesMixin


# 继承NamesMixin，里面有仅获取id和名称接口
# 在project模块也可调用
class EnvsViewSet(NamesMixin, viewsets.ModelViewSet):
    serializer_class = EnvsSerializers
    queryset = Envs.objects.all()

    # 接口为names时，替换序列化器类
    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNamesSerializers
        else:
            return super().get_serializer_class()
