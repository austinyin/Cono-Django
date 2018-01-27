"""
用户模型
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

from models.commonModel import WHETHER_CHOICES
from models.userModel import GENDER_CHOICES


class User(AbstractUser):
    """
    用户
    """
    phone = models.IntegerField(blank=True, null=True, unique=True, verbose_name="手机号码")
    self_intro = models.CharField(max_length=500, blank=True, null=True, verbose_name="个人简介")
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, verbose_name="性别")
    is_private = models.IntegerField(default=0, verbose_name="是否匿名")
    is_verified = models.IntegerField(default=0, choices=WHETHER_CHOICES, verbose_name="是否认证")
    is_influencer = models.IntegerField(default=0, choices=WHETHER_CHOICES, verbose_name="是否大V")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'user'

    def __str__(self):
        return self.username


class Visitor(models.Model):
    """
    览客
    """
    ip = models.CharField(max_length=50,verbose_name="ip地址")
    create_time = models.DateTimeField(auto_now=True, verbose_name="进入时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="变更时间")

    class Meta:
        verbose_name = '游客'
        verbose_name_plural = '游客'
        db_table = 'visitor'

    def __str__(self):
        return self.ip




