# from django.db import models
# from utils.basemodel import BaseModel
#
#
# class Interfaces(BaseModel):
#     name = models.CharField(verbose_name='接口名称', help_text='接口名称', max_length=50)
#     tester = models.CharField(verbose_name='测试人员', help_text='测试人员', max_length=10)
#     # a、如果需要创建一对多的外键，那么会在”多“的那一个模型类中定义外键字段
#     # b、如果创建的是一对多的关系，使用ForeignKey
#     # c、如果创建的是一对一的关系，可以在任何一个模型类使用OneToOneField
#     # d、如果创建的是多对多的关系，可以在任何一个模型类使用ManyToManyField
#     # e、ForeignKey第一个参数为必填参数，指定需要关联的父表模型类
#         # 方式一：直接使用父表模型类的引用
#         # 方式二：可以使用‘子应用名.父表模型类’（推荐）
#     # f、ForeignKey需要使用on_delete指定级联删除策略
#     # CASECADE：当父表数据删除时，相对应的从表数据会被自动删除
#     # SET_NULL：当父表数据删除时，相对应的从表数据会被自动设置为null值
#     # PROTECT：当父表数据删除时，如果有对应的从表数据，则会抛出异常
#     # SET_DEFAULT:当父表数据删除时，相对应的从表数据会被自动设置为默认值，还需要额外指定default=True
#     # 如果第一个参数，填self，则为自关联，eg：评论与子评论
#     projects = models.ForeignKey('projects.Projects', on_delete=models.CASCADE, verbose_name='所属项目',
#                                  help_text='所属项目')
#
#     class Meta:
#         db_table = 'tb_interfaces'
#         verbose_name = '接口表'
#         verbose_name_plural = '接口表'
#         # 按id升序排列
#         ordering = ['id']
#
#     # 打印类时调用此方法
#     def __str__(self):
#         return f'Interfaces({self.name})'