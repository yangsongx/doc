# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HelpQA',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('question', models.TextField(max_length=500, verbose_name='\u95ee\u9898')),
                ('answer', models.TextField(max_length=500, verbose_name='\u56de\u7b54')),
                ('author', models.CharField(max_length=50, null=True, blank=True)),
                ('level', models.IntegerField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now_add=True, db_column='modified')),
                ('audited', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u5e38\u89c1\u95ee\u9898',
                'db_table': 'help_qa',
                'managed': False,
                'verbose_name_plural': '\u5e38\u89c1\u95ee\u9898',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('mid', models.AutoField(serialize=False, primary_key=True)),
                ('owner', models.IntegerField(null=True, blank=True)),
                ('target', models.CharField(max_length=32, null=True, blank=True)),
                ('targetcode', models.CharField(max_length=32, null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'membership',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('resolution', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u8bbe\u5907\u7c7b\u578b',
                'db_table': 'model',
                'managed': False,
                'verbose_name_plural': '\u8bbe\u5907\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='id')),
                ('cid', models.IntegerField()),
                ('description', models.CharField(max_length=50, null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('pincode', models.CharField(max_length=50, null=True, db_column='PINcode', blank=True)),
                ('md5', models.CharField(max_length=50, null=True, blank=True)),
                ('size', models.IntegerField()),
                ('type', models.IntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('dirty', models.IntegerField(null=True, blank=True)),
                ('share', models.IntegerField(null=True, blank=True)),
                ('completed', models.DateTimeField(null=True, blank=True)),
                ('target', models.CharField(max_length=32, null=True, blank=True)),
                ('targetcode', models.CharField(max_length=32, null=True, blank=True)),
                ('idhash', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u5b9a\u5236\u5305',
                'db_table': 'packages',
                'managed': False,
                'verbose_name_plural': '\u5b9a\u5236\u5305',
            },
        ),
        migrations.CreateModel(
            name='PbCategory',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, db_column='ID')),
                ('category_name', models.CharField(max_length=30, db_column='CATEGORY_NAME')),
                ('category_desp', models.CharField(max_length=255, null=True, db_column='CATEGORY_DESP', blank=True)),
                ('last_modify_time', models.DateTimeField(null=True, db_column='LAST_MODIFY_TIME', blank=True)),
                ('category_pic_link', models.CharField(max_length=255, null=True, db_column='CATEGORY_PIC_LINK', blank=True)),
                ('type_id', models.BigIntegerField(null=True, db_column='TYPE_ID', blank=True)),
            ],
            options={
                'verbose_name': '\u9884\u7f6e\u8d44\u6e90\u5b50\u7c7b',
                'db_table': 'pb_category',
                'managed': False,
                'verbose_name_plural': '\u9884\u7f6e\u8d44\u6e90\u5b50\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='PbInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('res_name', models.CharField(max_length=60, verbose_name='\u540d\u79f0', db_column='RES_NAME')),
                ('res_author', models.CharField(max_length=60, verbose_name='\u4f5c\u8005', db_column='RES_AUTHOR')),
                ('res_desp', models.CharField(max_length=255, null=True, verbose_name='\u63cf\u8ff0', db_column='RES_DESP', blank=True)),
                ('res_length', models.BigIntegerField(null=True, verbose_name='\u6587\u4ef6\u5927\u5c0f', db_column='RES_LENGTH', blank=True)),
                ('res_file_path', models.CharField(max_length=200, verbose_name='\u4e0b\u8f7d\u8def\u5f84', db_column='RES_FILE_PATH')),
                ('res_download_num', models.BigIntegerField(null=True, verbose_name='\u4e0b\u8f7d\u6570\u91cf', db_column='RES_DOWNLOAD_NUM', blank=True)),
                ('res_recommend_level', models.BigIntegerField(null=True, verbose_name='\u63a8\u8350\u6307\u6570', db_column='RES_RECOMMEND_LEVEL', blank=True)),
                ('create_time', models.DateTimeField(null=True, verbose_name='\u521b\u5efa\u65f6\u95f4', db_column='CREATE_TIME', blank=True)),
                ('last_modify_time', models.DateTimeField(null=True, verbose_name='\u4fee\u6539\u65f6\u95f4', db_column='LAST_MODIFY_TIME', blank=True)),
                ('extra_info', models.CharField(max_length=128, null=True, verbose_name='\u9644\u52a0\u4fe1\u606f', db_column='EXTRA_INFO', blank=True)),
            ],
            options={
                'verbose_name': '\u9884\u7f6e\u8d44\u6e90',
                'db_table': 'pb_info',
                'managed': False,
                'verbose_name_plural': '\u9884\u7f6e\u8d44\u6e90',
            },
        ),
        migrations.CreateModel(
            name='PbType',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, db_column='ID')),
                ('type_name', models.CharField(max_length=20, db_column='TYPE_NAME')),
                ('display_name', models.CharField(max_length=30, db_column='DISPLAY_NAME')),
                ('type_desp', models.CharField(max_length=255, null=True, db_column='TYPE_DESP', blank=True)),
                ('last_modify_time', models.DateTimeField(null=True, db_column='LAST_MODIFY_TIME', blank=True)),
            ],
            options={
                'verbose_name': '\u9884\u7f6e\u8d44\u6e90\u5927\u7c7b',
                'db_table': 'pb_type',
                'managed': False,
                'verbose_name_plural': '\u9884\u7f6e\u8d44\u6e90\u5927\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Rawfiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('download_url', models.CharField(max_length=256, null=True, blank=True)),
                ('suffix', models.CharField(max_length=50, null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('crop', models.CharField(max_length=256, null=True, blank=True)),
                ('processed_url', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u5b9a\u5236\u539f\u59cb\u8d44\u6e90',
                'db_table': 'rawfiles',
                'managed': False,
                'verbose_name_plural': '\u5b9a\u5236\u539f\u59cb\u8d44\u6e90',
            },
        ),
    ]
