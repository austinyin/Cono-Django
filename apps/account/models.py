from django.db import models

from shared.choices.userModel import GENDER_CHOICES


class Regist(models.Model):
    """
    注册
    """
    username = models.CharField(max_length=20, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    first_name = models.CharField(max_length=10, verbose_name="姓")
    last_name = models.CharField(max_length=10, verbose_name="名")
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, verbose_name="性别")
    phone = models.IntegerField(null=True, blank=True, unique=True, verbose_name="手机")
    email = models.EmailField(null=True, blank=True, verbose_name="邮箱", unique=True)

    class Meta:
        verbose_name = '注册'
        verbose_name_plural = '注册'
        db_table = 'regist'

    def __str__(self):
        return self.username
