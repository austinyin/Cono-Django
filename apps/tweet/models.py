"""
发文
"""
import os

import re
from django.db import models

from Cono.settings import BASE_DIR
from apps.medium.models import TweetVideo, TweetImage
from apps.user.models import User
from shared.choices.tweetModel import TWEET_TYPE_CHOICES
from shared.constants.common import IMAGE_THUMBNAIL_TYPE, IMAGE_THUMBNAIL_SIZE
from util.file_process import image_scale, ffmpeg_video_screenshot


class Tweet(models.Model):
    """
    推文
    """
    text = models.TextField(null=True, blank=True, verbose_name="文字")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="发布者")
    short_code = models.CharField(max_length=100, unique=True, verbose_name="短码")
    type = models.IntegerField(default=1, choices=TWEET_TYPE_CHOICES, verbose_name="类型")
    images = models.ManyToManyField(TweetImage, related_name="tweet_image", blank=True, verbose_name="图片")
    video = models.ForeignKey(TweetVideo, null=True, blank=True, on_delete=models.CASCADE, verbose_name="视频")
    image_thumbnail = models.ForeignKey(TweetImage, null=True, related_name="tweet_image_thumbnail", blank=True,
                                        on_delete=models.CASCADE, verbose_name="略缩展示图")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '推文'
        verbose_name_plural = '推文'
        db_table = 'tweet'
        ordering = ('-create_time', '-update_time',)

    def __str__(self):
        return self.short_code

    def save_with_thumbnail(self):
        super(Tweet, self).save()  # 先调用父类的save,否则后面不能处理 self.images or self.video
        first_image = self.images.first()
        video_obj = self.video
        thumbnail_path = None
        if first_image:
            thumbnail_path = self.image_obj_scale_handle(first_image)
        if video_obj:
            thumbnail_path = self.video_capture_and_scale_handle(video_obj)

        self.image_thumbnail = TweetImage.objects.create(image=thumbnail_path,
                                                         describe='{} thumbImage'.format(self.short_code))
        super(Tweet, self).save()  # 保存截图

    def image_obj_scale_handle(self, image_obj):
        img_path, thumb_save_path = self.path_cac(image_obj.image)
        scaled_image_path = image_scale(IMAGE_THUMBNAIL_SIZE, img_path,thumb_save_path)
        return f"/media{str.split(scaled_image_path)[1]}"

    def video_capture_and_scale_handle(self, video_obj):
        video_path, thumb_save_path = self.path_cac(video_obj.video)
        scaled_image_path = ffmpeg_video_screenshot(video_path, thumb_save_path)
        return f"/media{str.split(scaled_image_path)[1]}"

    # thumbnail路径计算
    # file_path 返回相对路径
    def path_cac(self,file):
        file_path = "media/" + str(file)
        thumb_save_path = os.path.join(BASE_DIR, 'media/image/crop', '{}_thumbnail.jpg'.format(self.short_code))
        return file_path, thumb_save_path
