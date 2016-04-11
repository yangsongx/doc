#coding:utf-8

from __future__ import unicode_literals
from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

class RobotType(models.Model):
    description = models.CharField(max_length=255, blank=True,null=True)

#Only available for @AccountProfile::allow_reply is True
class WhiteNameList(models.Model):
    name_list = models.CharField(max_length=1024,blank=True,null=True)

class UserCustomization(models.Model):
    question = models.CharField(max_length=255, blank=True,null=True)
    answer = models.CharField(max_length=512, blank=True,null=True)

# TODO - ysx
# in order to give a quick/usable demo, currently use MySQL store this,
# in final product, we will move to MongoDB smoothly
class CorpusData(models.Model):
    question = models.CharField(max_length=255, blank=True,null=True)
    answer = models.CharField(max_length=512, blank=True,null=True)


class AccountProfile(models.Model):
    user_id = models.BigIntegerField(blank=True,null=True) # This is id from django's User model
    mail_act = models.CharField(max_length=256, blank=True)
    mail_act_expire = models.DateTimeField(blank=True,null=True)
    robot_id = models.ForeignKey(RobotType, blank=True, null=True)
    robot_alias = models.CharField(max_length=256, blank=True)
    robot_creation = models.DateTimeField(blank=True,null=True)
    allow_reply = models.BooleanField(default=True)
    list_reply = models.ForeignKey(WhiteNameList, blank=True, null=True)
    customization = models.ForeignKey(UserCustomization, blank=True, null=True)
    gender = models.BooleanField(default=True)
    address = models.CharField(max_length=255, blank=True,null=True)
