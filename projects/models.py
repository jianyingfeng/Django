from django.db import models
from utils.basemodel import BaseModel


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.BooleanField()


class Projects(BaseModel):
    # primary_key指定后，创建的数据表就不会自动生成一个id字段（一张表只会有一个主键id）
    # ids = models.IntegerField(primary_key=True, verbose_name='项目主键', help_text='项目主键')
    #a、CharField类型必须指定max_length参数（该字段的最大字节数），不传则存“”
    #b、unique=True（默认为False）可以给字段添加唯一约束
    name = models.CharField(max_length=20, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=10, verbose_name='项目名称', help_text='项目名称')
    #c、使用default指定默认值（如果前端在创建记录时，未传递该字段，则使用默认值）
    is_execute = models.BooleanField(default=True, verbose_name='项目是否启动（默认为启动）', help_text='项目是否启动（默认为启动）')
    #d、null=True指定前端创建数据时，可以指定该字段为null，默认null=False,DRF进行反序列化器输入时才有效
    #e、blank=True指定前端创建数据时，可以指定该字段为null，默认blank=False,DRF进行反序列化器输入时才有效
    desc = models.TextField(verbose_name='项目描述', help_text='项目描述', null=True, blank=True, default='')
    #f、auto_now_add=True（默认为false），在创建记录时，会把当前时间赋值给该字段
    #g、auto_now=True（默认为false），在更新记录时，会把当前时间赋值给该字段
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)



    #h、可以在任意一个模型类中创建Meta内部类，用于修改数据库的元数据信息
    class Meta:
        #i、db_table指定创建的数据表名称
        db_table = 'tb_projects'
        # i、verbose_name，verbose_name_plural（复数）指定表名称
        verbose_name = '项目表'
        verbose_name_plural = '项目表'
        # 按id升序排列
        ordering = ['id']

    # 打印类时调用此方法
    def __str__(self):
        return f'Projects({self.name})'