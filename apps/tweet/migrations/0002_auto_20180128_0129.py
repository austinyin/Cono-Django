# Generated by Django 2.0.1 on 2018-01-27 17:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tweet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(on_delete='SET_NULL', to=settings.AUTH_USER_MODEL, verbose_name='发布者'),
        ),
        migrations.AddField(
            model_name='tweet',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', to='tweet.TweetVideo', verbose_name='视频'),
        ),
    ]
