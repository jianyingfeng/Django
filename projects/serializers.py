from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from interfaces.models import Interfaces
from .models import Projects

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


# 自定义的序列化器类实际上也是Field的子类
# 所以自定义的序列化器类也可以作为另一个序列化器类中的字段
class InterfaceSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()


# 序列化类外自定义校验函数
# 参数为待校验的字段
# 校验不通过，则抛出serializers.ValidationError(),可自定义报错信息
# 再将函数名写到被校验字段的validators列表中
def is_contains(value):
    if '项目' not in value:
        raise serializers.ValidationError('项目名称中必须包含“项目”二字')


class ProjectSerializers(serializers.Serializer):
    id = serializers.IntegerField(label='项目id', help_text='项目id', min_value=1, max_value=1000, required=False)
    # 可以在序列化字段上使用validators参数指定自定义的校验规则
    # validators参数跟的是列表，可以指定多个校验规则
    # UniqueValidator校验器需要指定querset对数据进行校验，并通锅message指定报错信息
    # 校验的顺序：
    #   1、校验字段类型--》2、从左到右校验validators里面的规则--》3、从右到左校验其他规则（就算某项不通过也会一直校验下去）--》4、单个字段校验--》5、联合字段校验
    name = serializers.CharField(label='项目名称', help_text='项目名称', min_length=5, max_length=20,
                                 error_messages={'min_length':'最少为5位', 'max_length':'最长为20位', 'required':'该字段必填'},
                                 validators=[UniqueValidator(queryset=Projects.objects.all(), message='项目名称已存在'),
                                             is_contains])
    leader = serializers.CharField(label='项目负责人', help_text='项目负责人', default='mm')
    # 关联字段
    # 可以直接定义PrimaryKeyRelatedField来获取关联表的外键值
    # 字段名称默认为关联表模型类名称小写_set,关联模型类中的关联字段指定了related_name参数，则字段名使用这个
    # PrimaryKeyRelatedField字段要么指定read_only=True,要么指定queryset参数，否则会报错
    # 如果指定了read_only=True，那么该字段只做序列化输出
    # 如果指定了queryset参数，那么可以对入参进行校验，校验传入的参数是否存在于查询集中
    # 查到的关联字段一般会有多个值，所以需要指定many=True
    # interfaces_set = serializers.PrimaryKeyRelatedField(label='项目附属接口id', help_text='项目附属接口id', many=True,
    #                                                     queryset=Interfaces.objects.all(), write_only=True)

    # StringRelatedField字段可以将关联模型类中__str__方法中的返回值输出
    # 自动指定了read_only=True,该字段仅格式化输出
    # interfaces_set = serializers.StringRelatedField(many=True)

    # 使用SlugRelatedField字段，可以任意指定关联模型类的某个字段作为这个字段的值
    # 如果指定了read_only=True,该字段仅格式化输出
    # 如果该字段需要输入，则必须指定queryset参数，同时关联参数必须有唯一约束
    # interfaces_set = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Interfaces.objects.all())

    interfaces_set = InterfaceSerializers(label='项目附属接口id', help_text='项目附属接口id', many=True ,required=False)
    # format参数可以对时间进行格式化输出
    update_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format='%Y-%m-%d %H:%M:%S', required=False)
    create_time = serializers.DateTimeField(label='创建时间', help_text='创建时间', format='%Y-%m-%d %H:%M:%S', required=False)

    # 单个字段校验
    # 写在序列化类里面的校验方法名称必须为validate_字段名称
    # 且校验通过，必须将字段返回，不返回则会返回None，在写库的时候会报错
    # 只有当序列化类外的校验以及validators的校验通过之后，才会走这个校验
    def validate_name(self, attr:str):
        if not attr.endswith('项目'):
            raise serializers.ValidationError('项目名称必须以“项目”结尾')
        return attr

    # 联合字段校验
    # 方法名称必须为validate，attrs是个字典，
    # 最后必须返回
    def validate(self, attrs:dict):
        if not (len(attrs.get('leader'))>=4 and attrs.get('is_execute') == True):
            raise serializers.ValidationError('项目负责人长度小于4位或is_execute不为True')
        return attrs