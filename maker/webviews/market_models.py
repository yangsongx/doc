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


class ResourceCategory(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    category_parent_id = models.BigIntegerField(db_column='CATEGORY_PARENT_ID')  # Field name made lowercase.
    category_name = models.CharField(db_column='CATEGORY_NAME',
                                     max_length=30)  # Field name made lowercase.
    category_desp = models.TextField(db_column='CATEGORY_DESP',
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    category_icon = models.TextField(db_column='CATEGORY_ICON',
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    category_enum = models.IntegerField(db_column='CATEGORY_ENUM')  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    category_recommend_level = models.BigIntegerField(
        db_column='CATEGORY_RECOMMEND_LEVEL',
        blank=True,
        null=True)  # Field name made lowercase.
    category_pic = models.TextField(db_column='CATEGORY_PIC',
                                    blank=True,
                                    null=True)  # Field name made lowercase.
    category_pic_link = models.TextField(db_column='CATEGORY_PIC_LINK',
                                         blank=True,
                                         null=True)  # Field name made lowercase.
    type_id = models.BigIntegerField(db_column='TYPE_ID',
                                     blank=True,
                                     null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESOURCE_CATEGORY'


class ResourceInfo(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    res_pkg = models.CharField(db_column='RES_PKG',
                               max_length=60,
                               blank=True,
                               null=True)  # Field name made lowercase.
    res_name = models.CharField(db_column='RES_NAME',
                                max_length=60)  # Field name made lowercase.
    res_version = models.CharField(db_column='RES_VERSION',
                                   max_length=20,
                                   blank=True,
                                   null=True)  # Field name made lowercase.
    res_version_code = models.IntegerField(db_column='RES_VERSION_CODE',
                                           blank=True,
                                           null=True)  # Field name made lowercase.
    res_desp = models.TextField(db_column='RES_DESP',
                                blank=True,
                                null=True)  # Field name made lowercase.
    res_icon = models.TextField(db_column='RES_ICON',
                                blank=True,
                                null=True)  # Field name made lowercase.
    res_length = models.BigIntegerField(db_column='RES_LENGTH',
                                        blank=True,
                                        null=True)  # Field name made lowercase.
    res_summary = models.CharField(db_column='RES_SUMMARY',
                                   max_length=100)  # Field name made lowercase.
    large_icon_path = models.TextField(db_column='LARGE_ICON_PATH',
                                       blank=True,
                                       null=True)  # Field name made lowercase.
    res_file_path = models.CharField(db_column='RES_FILE_PATH',
                                     max_length=200,
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    res_file_hash = models.CharField(db_column='RES_FILE_HASH',
                                     max_length=255,
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    res_price = models.FloatField(db_column='RES_PRICE',
                                  blank=True,
                                  null=True)  # Field name made lowercase.
    res_download_num = models.BigIntegerField(db_column='RES_DOWNLOAD_NUM',
                                              blank=True,
                                              null=True)  # Field name made lowercase.
    res_recommend_level = models.BigIntegerField(
        db_column='RES_RECOMMEND_LEVEL',
        blank=True,
        null=True)  # Field name made lowercase.
    is_deleted = models.IntegerField(db_column='IS_DELETED',
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    license = models.CharField(db_column='LICENSE',
                               max_length=60,
                               blank=True,
                               null=True)  # Field name made lowercase.
    compatible = models.IntegerField(db_column='COMPATIBLE',
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    res_keywords = models.CharField(db_column='RES_KEYWORDS',
                                    max_length=40,
                                    blank=True,
                                    null=True)  # Field name made lowercase.
    res_other2 = models.CharField(db_column='RES_OTHER2',
                                  max_length=255,
                                  blank=True,
                                  null=True)  # Field name made lowercase.
    min_sdkversion = models.IntegerField(db_column='MIN_SDKVERSION',
                                         blank=True,
                                         null=True)  # Field name made lowercase.
    native_codes = models.CharField(db_column='NATIVE_CODES',
                                    max_length=20,
                                    blank=True,
                                    null=True)  # Field name made lowercase.
    permissions = models.TextField(db_column='PERMISSIONS',
                                   blank=True,
                                   null=True)  # Field name made lowercase.
    features = models.TextField(db_column='FEATURES',
                                blank=True,
                                null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME',
                                       blank=True,
                                       null=True)  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    res_category = models.ForeignKey(ResourceCategory,
                                     db_column='RES_CATEGORY_ID',
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    res_type = models.ForeignKey('ResourceType',
                                 db_column='RES_TYPE_ID',
                                 blank=True,
                                 null=True)  # Field name made lowercase.
    res_source = models.ForeignKey('ResourceSource',
                                   db_column='RES_SOURCE_ID',
                                   blank=True,
                                   null=True)  # Field name made lowercase.
    file_size = models.BigIntegerField(db_column='FILE_SIZE',
                                       blank=True,
                                       null=True)  # Field name made lowercase.
    province_id = models.IntegerField(db_column='PROVINCE_ID',
                                      blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESOURCE_INFO'


class ResourceSource(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    source_name = models.CharField(db_column='SOURCE_NAME',
                                   max_length=60)  # Field name made lowercase.
    source_phone_number = models.CharField(db_column='SOURCE_PHONE_NUMBER',
                                           max_length=40,
                                           blank=True,
                                           null=True)  # Field name made lowercase.
    source_other1 = models.CharField(db_column='SOURCE_OTHER1',
                                     max_length=255,
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    source_other2 = models.CharField(db_column='SOURCE_OTHER2',
                                     max_length=255,
                                     blank=True,
                                     null=True)  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESOURCE_SOURCE'


class ResourceStar(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    res = models.ForeignKey(ResourceInfo,
                            db_column='RES_ID')  # Field name made lowercase.
    star_num_sum = models.BigIntegerField(db_column='STAR_NUM_SUM',
                                          blank=True,
                                          null=True)  # Field name made lowercase.
    star_times_sum = models.BigIntegerField(db_column='STAR_TIMES_SUM',
                                            blank=True,
                                            null=True)  # Field name made lowercase.
    recommend_other1 = models.CharField(db_column='RECOMMEND_OTHER1',
                                        max_length=255,
                                        blank=True,
                                        null=True)  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESOURCE_STAR'


class ResourceType(models.Model):
    id = models.BigIntegerField(db_column='ID',
                                primary_key=True)  # Field name made lowercase.
    type_name = models.CharField(db_column='TYPE_NAME',
                                 unique=True,
                                 max_length=20)  # Field name made lowercase.
    display_name = models.CharField(db_column='DISPLAY_NAME',
                                    max_length=30)  # Field name made lowercase.
    type_desp = models.TextField(db_column='TYPE_DESP',
                                 blank=True,
                                 null=True)  # Field name made lowercase.
    recommend_other1 = models.CharField(db_column='RECOMMEND_OTHER1',
                                        max_length=255,
                                        blank=True,
                                        null=True)  # Field name made lowercase.
    last_modify_time = models.DateTimeField(db_column='LAST_MODIFY_TIME',
                                            blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESOURCE_TYPE'
