"""
关系
"""
from django.db import models

from apps.user.models import User

from shared.choices.commonModel import BOOLEAN_CHOICES


class PersonRelations(models.Model):
    """
    人物关系
    """
    act_one = models.ForeignKey(User, related_name='act_person', on_delete=models.CASCADE, verbose_name="行为方")
    target_one = models.ForeignKey(User, related_name='target_person', on_delete=models.CASCADE, verbose_name="目标")
    is_follow = models.BooleanField(default=False, choices=BOOLEAN_CHOICES, verbose_name="是否关注")
    is_block = models.BooleanField(default=False, choices=BOOLEAN_CHOICES, verbose_name="是否屏蔽")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '人物关系'
        verbose_name_plural = '人物关系'
        db_table = 'person_relations'
        unique_together = ('act_one', 'target_one',)

    def __str__(self):
        return self.act_one.username


class TweetRelations(models.Model):
    """
    推文关系
    """
    user = models.ForeignKey(User, verbose_name="收藏者", on_delete=models.CASCADE)
    tweet = models.ForeignKey('tweet.Tweet', verbose_name="收藏文章", on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False, choices=BOOLEAN_CHOICES, verbose_name="是否点赞")
    is_collect = models.BooleanField(default=False, choices=BOOLEAN_CHOICES, verbose_name="是否收藏")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '推文关系'
        verbose_name_plural = '推文关系'
        db_table = 'tweet_relations'
        unique_together = ('user', 'tweet',)

    def __str__(self):
        return 'tweetId: {} userId: {}'.format(str(self.tweet.id), str(self.user.id))


class Comment(models.Model):
    """
    推文评论
    """
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, verbose_name="评论者", on_delete=models.CASCADE)
    tweet = models.ForeignKey('tweet.Tweet', verbose_name="被评论文章", on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '推文评论'
        verbose_name_plural = '推文评论'
        db_table = 'comment'

    def __str__(self):
        return self.text


class TweetSign(models.Model):
    """
    推文@
    """
    act_one = models.ForeignKey(User, related_name='tweet_sign_act_person', on_delete=models.CASCADE,
                                verbose_name="行为方")
    tweet = models.ForeignKey('tweet.Tweet', on_delete=models.CASCADE, verbose_name="文章")
    target_one = models.ForeignKey(User, related_name='tweet_sign_target_person', on_delete=models.CASCADE,
                                   verbose_name="目标")
    text = models.CharField(max_length=1000, null=True, blank=True, verbose_name="文字")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '推文标记'
        verbose_name_plural = '推文标记'
        db_table = 'tweet_sign'

    def __str__(self):
        return self.act_one.username


class CommentSign(models.Model):
    """
    推文@
    """
    act_one = models.ForeignKey(User, related_name='comment_sign_act_person', on_delete=models.CASCADE,
                                verbose_name="行为方")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="评论")
    target_one = models.ForeignKey(User, related_name='comment_sign_target_person', on_delete=models.CASCADE,
                                   verbose_name="目标")
    text = models.CharField(max_length=1000, null=True, blank=True, verbose_name="文字")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '评论标记'
        verbose_name_plural = '评论标记'
        db_table = 'comment_sign'

    def __str__(self):
        return self.act_one.username


class Notices(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment, blank=True, verbose_name="评论")
    commentSigns = models.ManyToManyField(CommentSign, blank=True, verbose_name="评论标记")
    tweetSigns = models.ManyToManyField(TweetSign, blank=True, verbose_name="tweet标记")
    tweetLikes = models.ManyToManyField(TweetRelations, blank=True, verbose_name="tweet点赞")
    personFollows = models.ManyToManyField(PersonRelations, blank=True, verbose_name="person follow")
    period = models.IntegerField(default=7, verbose_name="周期(day)")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        db_table = 'notice'

# class Notice(models.Model):
#     user = models.ForeignKey(User,verbose_name="用户", on_delete=models.CASCADE)
#     type = models.IntegerField(choices=NOTICE_CHOICES,verbose_name="类型")
#     comment = models.ForeignKey(Comment, blank=True, verbose_name="评论",on_delete=models.CASCADE)
#     comment_sign = models.ForeignKey(CommentSign, blank=True, verbose_name="评论标记",on_delete=models.CASCADE)
#     tweet_sign = models.ForeignKey(TweetSign, blank=True, verbose_name="推文标记",on_delete=models.CASCADE)
#     tweet_like = models.ForeignKey(TweetRelations, blank=True, verbose_name="推文点赞",on_delete=models.CASCADE)
#     person_follow = models.ForeignKey(PersonRelations, blank=True, verbose_name="人际追随",on_delete=models.CASCADE)
#     update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name="变更时间")
#
#     class Meta:
#         verbose_name = '通知'
#         verbose_name_plural = '通知'
#         db_table = 'notice'
