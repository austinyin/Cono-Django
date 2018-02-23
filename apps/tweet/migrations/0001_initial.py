# Generated by Django 2.0.1 on 2018-02-20 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medium', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='文字')),
                ('short_code', models.CharField(max_length=100, unique=True, verbose_name='短码')),
                ('type', models.IntegerField(choices=[(1, '图片'), (2, '视频')], default=1, verbose_name='类型')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('images', models.ManyToManyField(blank=True, to='medium.TweetImage', verbose_name='图片')),
            ],
            options={
                'verbose_name': '推文',
                'verbose_name_plural': '推文',
                'db_table': 'tweet',
                'ordering': ('-create_time', '-update_time'),
            },
        ),
    ]
