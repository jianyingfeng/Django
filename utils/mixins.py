import os
from datetime import datetime

from django.conf import settings
from rest_framework.decorators import action

from utils import common
from envs.models import Envs


class NamesMixin:
    # 仅获取环境id和名称的接口
    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # 接口为names时，不作过滤
    def filter_queryset(self, queryset):
        if self.action == 'names':
            return queryset
        else:
            return super().filter_queryset(queryset)

    # 接口为names时，不作分页
    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)


class RunMixin:
    def execute(self,instance, qs, request):
        # 获取env_id
        serializer = self.get_serializer(data=request.data)
        # 校验通过返回True，不通过则返回报错信息
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)
        # 创建时间戳目录
        testcase_dir_path = os.path.join(settings.PROJECT_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        os.makedirs(testcase_dir_path)
        # 创建以项目名命名的目录
        # 创建以debugtalk.py，yaml文件
        for obj in qs:
            common.generate_testcase_file(obj, env, testcase_dir_path)
        # 运行用例并生成测试报告
        return common.run(instance, testcase_dir_path)
