"""
关系
"""
from django.db import models

from apps.tweet.models import Tweet
from apps.user.models import User
from models.commonModel import WHETHER_CHOICES


class PersonRelations(models.Model):
    """
    人物关系
    """
    act_one = models.ForeignKey(User, related_name='act_person', on_delete='SET_NULL', verbose_name="行为方")
    target_one = models.ForeignKey(User, related_name='target_person', on_delete='SET_NULL', verbose_name="目标")
    is_block = models.IntegerField(default=0, choices=WHETHER_CHOICES, verbose_name="是否屏蔽")
    is_friend = models.IntegerField(default=0, choices=WHETHER_CHOICES, verbose_name="是否关注")

    class Meta:
        verbose_name = '人物关系'
        verbose_name_plural = '人物关系'
        db_table = 'person_relations'

    def __str__(self):
        return self.act_one.username


class Comment(models.Model):
    """
    推文评论
    """
    text = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")
    user = models.ForeignKey(User, verbose_name="评论者", on_delete='SET_NULL')
    tweet = models.ForeignKey(Tweet, verbose_name="被评论文章", on_delete='SET_NULL')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'comment'

    def __str__(self):
        return self.text


class TweetSign(models.Model):
    """
    推文@
    """
    act_one = models.ForeignKey(User, related_name='sign_act_person', on_delete='SET_NULL', verbose_name="行为方")
    tweet = models.ForeignKey(Tweet, on_delete='SET_NULL', verbose_name="文章")
    target = models.ForeignKey(User, related_name='sign_target_person', on_delete='SET_NULL', verbose_name="目标")
    text = models.CharField(max_length=1000,null=True,blank=True,verbose_name="文字")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '标记'
        verbose_name_plural = '标记'
        db_table = 'tweet_sign'

    def __str__(self):
        return self.act_one
