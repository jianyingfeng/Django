from rest_framework import serializers


# 序列化类：
# DRF中的序列化模块，在子应用下新建该py文件即可
# 文件名建议命名为serializers.py
# 1、定义的字段名称必须与模型类字段名称一致
# 2、定义了哪些字段，就会返回哪些字段，同时前端也必须传递这些字段值
# label和help_text相当于模型类中的verbose_name和help_text字段
# min_value和max_value指定参数的最小值和最大值
# min_length和max_length指定最小长度和最大长度
# required默认为True，即必填
# write_only=True，前端会传递，但是不会返回给前端，默认为False
# read_only_True，前端不用传递，传递了也不起作用，但是会返回给前端，默认为False
# allow_null=True,前端可以传null，默认为False
# allow_blank=True,前端可以传""，默认为False，只有CharField字段才能指定
# default指定默认值，只有在前端既不传键，也不传值的时候生效（传null和“”不生效）
class ProjectSerializers(serializers.Serializer):
    id = serializers.IntegerField(label='项目id', help_text='项目id', min_value=1, max_value=1000, required=False)
    name = serializers.CharField(label='项目名称', help_text='项目名称', min_length=5, max_length=20, read_only=True)
    leader = serializers.CharField(label='项目负责人', help_text='项目负责人', default='mm')
