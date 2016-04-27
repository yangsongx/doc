#coding:utf-8

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Model(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=True, null=True)
    resolution = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'model'
        verbose_name = u'设备类型'
        verbose_name_plural = u'设备类型'

    def __unicode__(self):
        return self.name


class Packages(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    mod = models.ForeignKey(Model)
    cid = models.IntegerField()
    description = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    pincode = models.CharField(db_column='PINcode',
                               max_length=50,
                               blank=True,
                               null=True)  # Field name made lowercase.
    md5 = models.CharField(max_length=50, blank=True, null=True)
    size = models.IntegerField()
    type = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    dirty = models.IntegerField(blank=True, null=True)
    share = models.IntegerField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)
    target = models.CharField(max_length=32, blank=True, null=True)
    targetcode = models.CharField(max_length=32, blank=True, null=True)
    idhash = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'packages'
        verbose_name = u'定制包'
        verbose_name_plural = u'定制包'

    def __unicode__(self):
        return str(self.id)


class PbCategory(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='CATEGORY_NAME',
                                     max_length=30)  # Field name made lowercase.
    category_desp = models.CharField(db_column='CATEGORY_DESP',
                                     max_length=255,
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    category_pic_link = models.CharField(db_column='CATEGORY_PIC_LINK',
                                         max_length=255,
                                         blank=True,
                                         null=True)  # Field name made lowercase.
    type_id = models.BigIntegerField(db_column='TYPE_ID',
                                     blank=True,
                                     null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pb_category'
        verbose_name = u'预置资源子类'
        verbose_name_plural = u'预置资源子类'

    def __unicode__(self):
        return self.category_desp


class PbInfo(models.Model):
    #id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    res_name = models.CharField(db_column='RES_NAME',
                                max_length=60,
                                verbose_name=u'名称')  # Field name made lowercase.
    res_author = models.CharField(db_column='RES_AUTHOR',
                                  max_length=60,
                                  verbose_name='作者')  # Field name made lowercase.
    res_desp = models.CharField(db_column='RES_DESP',
                                max_length=255,
                                blank=True,
                                null=True,
                                verbose_name='描述')  # Field name made lowercase.
    res_length = models.BigIntegerField(db_column='RES_LENGTH',
                                        blank=True,
                                        null=True,
                                        verbose_name='文件大小')  # Field name made lowercase.
    res_file_path = models.CharField(db_column='RES_FILE_PATH',
                                     max_length=200,
                                     verbose_name='下载路径')  # Field name made lowercase.
    res_download_num = models.BigIntegerField(db_column='RES_DOWNLOAD_NUM',
                                              blank=True,
                                              null=True,
                                              verbose_name='下载数量')  # Field name made lowercase.
    res_recommend_level = models.BigIntegerField(
        db_column='RES_RECOMMEND_LEVEL',
        blank=True,
        null=True,
        verbose_name='推荐指数')  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME',
                                       blank=True,
                                       null=True,
                                       verbose_name='创建时间')  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True,
                                            verbose_name='修改时间')  # Field name made lowercase.
    res_category = models.ForeignKey(PbCategory,
                                     db_column='RES_CATEGORY_ID',
                                     verbose_name='小类')  # Field name made lowercase.
    res_type = models.ForeignKey('PbType',
                                 db_column='RES_TYPE_ID',
                                 verbose_name='大类')  # Field name made lowercase.
    extra_info = models.CharField(db_column='EXTRA_INFO',
                                  max_length=128,
                                  blank=True,
                                  null=True,
                                  verbose_name='附加信息')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pb_info'
        verbose_name = u'预置资源'
        verbose_name_plural = u'预置资源'

    def __unicode__(self):
        return str(self.id)


class PbType(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    type_name = models.CharField(db_column='TYPE_NAME',
                                 max_length=20)  # Field name made lowercase.
    display_name = models.CharField(db_column='DISPLAY_NAME',
                                    max_length=30)  # Field name made lowercase.
    type_desp = models.CharField(db_column='TYPE_DESP',
                                 max_length=255,
                                 blank=True,
                                 null=True)  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.

    def __unicode__(self):
        return self.type_name

    class Meta:
        managed = False
        db_table = 'pb_type'
        verbose_name = u'预置资源大类'
        verbose_name_plural = u'预置资源大类'


class Rawfiles(models.Model):
    pb_type = models.ForeignKey(PbType,
                                db_column='pb_type_ID')  # Field name made lowercase.
    pb_info = models.ForeignKey(PbInfo,
                                db_column='pb_info_ID')  # Field name made lowercase.
    pac = models.ForeignKey(Packages)
    name = models.CharField(max_length=256, blank=True, null=True)
    download_url = models.CharField(max_length=256, blank=True, null=True)
    suffix = models.CharField(max_length=50, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    crop = models.CharField(max_length=256, blank=True, null=True)
    processed_url = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rawfiles'
        verbose_name = u'定制原始资源'
        verbose_name_plural = u'定制原始资源'


class HelpQA(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField('问题', max_length=500, )
    answer = models.TextField('回答', max_length=500, )
    author = models.CharField(max_length=50, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    modified = models.DateTimeField(auto_now_add=True, db_column='modified')
    audited = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'help_qa'
        verbose_name = u'常见问题'
        verbose_name_plural = u'常见问题'

class Membership(models.Model):
    id = models.AutoField(primary_key=True)
    package = models.ForeignKey('Packages')
    owner = models.IntegerField(blank=True, null=True)
    target = models.CharField(max_length=32, blank=True, null=True)
    targetcode = models.CharField(max_length=32, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    cid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membership'
