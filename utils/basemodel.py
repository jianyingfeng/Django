from django.db import models


# 公共类（存储公共字段）
class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='主键', help_text='主键')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        # 在内部类Meta中，一旦指定abstract = True，那么当前模型类为抽象模型类，在迁移时不会创建表，仅仅是为了供其他类继承
        abstract = True