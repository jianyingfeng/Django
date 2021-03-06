import json

from rest_framework import viewsets
from rest_framework.response import Response

from testcases.models import Testcases
from testcases.serializers import TestcasesSerializer


class TestcasesViewSet(viewsets.ModelViewSet):
    queryset = Testcases.objects.all()
    serializer_class = TestcasesSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        param_dict = json.loads(instance.request)['test']['request'].get('params')
        param_list = []
        if param_dict:
            for k, v in param_dict.items():
                param_list.append({'key': k, 'value': v})

        header_dict = json.loads(instance.request)['test']['request'].get('headers')
        header_list = []
        if header_dict:
            for k, v in header_dict.items():
                header_list.append({'key': k, 'value': v})

        variable_list = json.loads(instance.request)['test']['variables']
        variable_list_new = []
        if variable_list:
            for item in variable_list:
                variable_list_new.append(
                    {'key': list(item.keys())[0],
                     'value': list(item.values())[0],
                     'param_type': 'string' if str(type(list(item.values())[0]))[8:-2] == 'str' else
                     str(type(list(item.values())[0]))[8:-2]}
                )

        extract_list = json.loads(instance.request)['test'].get('extract')
        extract_list_new = []
        if extract_list:
            for item in extract_list:
                extract_list_new.append({'key': list(item.keys())[0],
                                         'value': list(item.values())[0]})

        validate_list = json.loads(instance.request)['test'].get('validate')
        validate_list_new = []
        if validate_list:
            for item in validate_list:
                validate_list_new.append(
                    {'key': item.get('check'),
                     'value': item.get('expected'),
                     'comparator': item.get('comparator'),
                     'param_type': 'string' if str(type(item.get('expected')))[8:-2] == 'str'
                     else str(type(item.get('expected')))[8:-2]
                     })

        parameterized_list = json.loads(instance.request)['test'].get('parameters')
        parameterized_list_new = []
        if parameterized_list:
            for item in parameterized_list:
                parameterized_list_new.append({'key': list(item.keys())[0],
                                               'value': str(list(item.values())[0])})

        setup_hooks_list = json.loads(instance.request)['test'].get('setup_hooks')
        setup_hooks_list_new = []
        if setup_hooks_list:
            for item in setup_hooks_list:
                setup_hooks_list_new.append({'key': item})

        teardown_hooks_list = json.loads(instance.request)['test'].get('teardown_hooks')
        teardown_hooks_list_new = []
        if teardown_hooks_list:
            for item in teardown_hooks_list:
                teardown_hooks_list_new.append({'key': item})

        response = {
            'author': instance.author,
            'testcase_name': instance.name,
            'selected_configure_id': json.loads(instance.include)['config'],
            'selected_interface_id': instance.interface_id,
            # ??????????????????interface_id??????????????????
            # 'selected_project_id': Projects.objects.get(
            #     interfaces__id=instance.interface_id
            # ).id,
            # ??????????????????pk??????????????????
            # 'selected_project_id': Projects.objects.get(
            #     interfaces__testcases__id=kwargs['pk']
            # ).id,
            # ????????????
            'selected_project_id': instance.interface.project.id,
            'selected_testcase_id': json.loads(instance.include)['testcases'],
            'method': json.loads(instance.request)['test']['request']['method'],
            'url': json.loads(instance.request)['test']['request']['url'],
            'param': param_list,
            'header': header_list,
            # 'variable': json.loads(instance.request)['test']['variables'],
            # ?????????globalVar?????????variable??????
            'variable': variable_list_new,
            # null?????????None???
            'jsonVariable': str(json.loads(instance.request)['test']['request'].get('json')),
            'extract': extract_list_new,
            'validate': validate_list_new,
            # 'globalVar': ?????????
            'parameterized': parameterized_list_new,
            'setup_Hooks': setup_hooks_list_new,
            'teardown_Hooks': teardown_hooks_list_new

        }
        return Response(response)
