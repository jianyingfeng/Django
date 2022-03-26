import json
from rest_framework import viewsets
from rest_framework.response import Response

from configures.models import Configures
from configures.serializers import ConfigSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Configures.objects.all()
    serializer_class = ConfigSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        header_dict = json.loads(instance.request)['config']['request'].get('headers')
        header_list = []
        if header_dict:
            for k, v in header_dict.items():
                header_list.append({'key': k, 'value': v})

        globalvar_list = json.loads(instance.request)['config'].get('variables')
        globalvar_list_new = []
        if globalvar_list:
            for item in globalvar_list:
                globalvar_list_new.append(
                    {'key': list(item.keys())[0],
                     'value': list(item.values())[0],
                     'param_type': 'string' if str(type(list(item.values())[0]))[8:-2] == 'str' else
                     str(type(list(item.values())[0]))[8:-2]}
                )

        response = {
            'author': instance.author,
            'configure_name': instance.name,
            'selected_project_id': instance.interface.project.id,
            'selected_interface_id': instance.interface_id,
            'selected_configure_id': instance.id,
            'header': header_list,
            'globalVar': globalvar_list_new
        }
        return Response(response)
