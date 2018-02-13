"""
发文
"""
from django.db import models

from apps.medium.models import TweetVideo, TweetImage
from apps.user.models import User
from shared.choices.tweetModel import TWEET_TYPE_CHOICES
from util.model_tools.file_upload import common_upload_path_handler




class Tweet(models.Model):
    """
    推文
    """
    text = models.TextField(null=True, blank=True, verbose_name="文字")
    user = models.ForeignKey(User, on_delete="SET_NULL", verbose_name="发布者")
    short_code = models.CharField(max_length=100, unique=True, verbose_name="短码")
    type = models.IntegerField(default=1, choices=TWEET_TYPE_CHOICES, verbose_name="类型")
    images = models.ManyToManyField(TweetImage, blank=True, verbose_name="图片")
    video = models.ForeignKey(TweetVideo, null=True, blank=True, on_delete="SET_NULL", verbose_name="视频")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

    class Meta:
        verbose_name = '推文'
        verbose_name_plural = '推文'
        db_table = 'tweet'
        ordering = ('-update_time', '-create_time',)

    def __str__(self):
        return self.short_code
