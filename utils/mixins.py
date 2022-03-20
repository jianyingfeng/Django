from rest_framework.decorators import action
from envs.serializers import EnvsNamesSerializers


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
