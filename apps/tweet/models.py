"""
发文
"""
from django.db import models

from apps.user.models import User
from models.tweetModel import TWEET_TYPE_CHOICES


class TweetImage(models.Model):
    """
    推文图片
    """
    image = models.ImageField(verbose_name="图片")
    describe = models.CharField(max_length=200, verbose_name="描述")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片'
        db_table = 'tweet_image'

    def __str__(self):
        return self.describe


class TweetVideo(models.Model):
    """
    推文视频
    """
    image = models.FileField(verbose_name="视频")
    describe = models.CharField(max_length=200, verbose_name="描述")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = '视频'
        db_table = 'tweet_video'

    def __str__(self):
        return self.describe


class Tweet(models.Model):
    """
    推文
    """
    text = models.TextField(blank=True, null=True, verbose_name="文字")
    user = models.ForeignKey(User, on_delete="SET_NULL", verbose_name="发布者")
    short_code = models.CharField(max_length=100, unique=True, verbose_name="短码")
    type = models.IntegerField(default=1, choices=TWEET_TYPE_CHOICES, verbose_name="类型")
    images = models.ManyToManyField(TweetImage, verbose_name="图片")
    video = models.ForeignKey(TweetVideo, null=True, blank=True, on_delete="SET_NULL", verbose_name="视频")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

    class Meta:
        verbose_name = '发文'
        verbose_name_plural = '发文'
        db_table = 'tweet'

    def __str__(self):
        return self.short_code
