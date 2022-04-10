from rest_framework import serializers

from projects.models import Projects
from interfaces.models import Interfaces
from envs.models import Envs


# 校验id值是否存在
class IsIdExists:
    def __init__(self, id_type):
        self.id_type = id_type

    def __call__(self, kw):
        if self.id_type == 'project':
            if not Projects.objects.filter(id=kw).exists():
                raise serializers.ValidationError(f'pid：{kw}不存在')
        elif self.id_type == 'interface':
            if not Interfaces.objects.filter(id=kw).exists():
                raise serializers.ValidationError(f'iid：{kw}不存在')
        elif self.id_type == 'env':
            if not Envs.objects.filter(id=kw).exists():
                raise serializers.ValidationError(f'env_id：{kw}不存在')
