import json

from django.http.response import StreamingHttpResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from reports.models import Reports
from reports.serializers import ReportsModelSerializer


class ReportViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer

    # 重写retrieve方法
    # 由于没有调用父类的retrieve方法，所以执行时不会调用序列化器类中的to_representation方法
    def retrieve(self, request, *args, **kwargs):
        instance = super().get_object()
        response = {
            'id': instance.id,
            'summary': json.loads(instance.summary)
        }
        return Response(response)

    @action(methods=['GET'], detail=True)
    def download(self, request, *args, **kwargs):
        # 获取报告html源码
        instance = self.get_object()
        # 是字符串类型
        print(type(instance.html))
        # 将源码转化为生成器对象
        iter_data = iter(instance.html)
        # 生成StreamingHttpResponse对象
        response = StreamingHttpResponse(iter(iter_data))
        # 添加响应头数据
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachment;filename*=UTF-8''{instance.name + '.html'}"
        return response
