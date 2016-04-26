#coding:utf-8

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

# 2016-04-14 try map with the models.User, as the top-single model used
# in this project
GENDER_CHOICES = (
        (u'1', '男'),
        (u'0', '女'),
 )

class AccountProfile(models.Model):

    user = models.OneToOneField(User,unique=True) # This is id from django's User model
    mail_act = models.CharField(max_length=256, blank=True)
    mail_act_expire = models.DateTimeField(blank=True,null=True)
#allow_reply = models.BooleanField(default=True)
#   list_reply = models.ForeignKey(WhiteNameList, blank=True, null=True)
    # gender = models.BooleanField(default=True)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES, default=u'1')
    address = models.CharField(max_length=255, blank=True,null=True)
    nickname = models.CharField(max_length=32, blank=True,null=True)
    phone_number = models.CharField(max_length=20, blank=True,null=True)


    def __unicode__(self):
        return unicode(self.user)


class WhiteNameList(models.Model):
    name_list = models.CharField(max_length=1024,blank=True,null=True)
    owner = models.ForeignKey(User, blank=True, null=True)

#FIXME - this should obsoleted as we use @CorpusData?
class UserCustomization(models.Model):
    question = models.CharField(max_length=255, blank=True,null=True)
    answer = models.CharField(max_length=512, blank=True,null=True)

class Robot(models.Model):
    description = models.CharField(max_length=255, blank=True,null=True)
    rob_sex = models.BooleanField(default=True)
    rob_age = models.IntegerField(blank=True, null=True)
    rob_alias = models.CharField(max_length=256, blank=True)
    rob_creation = models.DateTimeField(auto_now_add=True)
    rob_modification = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, blank=True, null=True)
#
# TODO - ysx
# in order to give a quick/usable demo, currently use MySQL store this,
# in final product, we will move to MongoDB smoothly
class CorpusData(models.Model):
    question = models.CharField(max_length=255, blank=False,null=False)
    answer = models.CharField(max_length=1024, blank=False,null=False)
    owner = models.ForeignKey(AccountProfile, blank=False, null=False)

#FIXME - temp put in MySQL, will moved to MongoDB smoothly in the future
class UserMessageData(models.Model):
    q = models.CharField(max_length=255, blank=True,null=True)
    a = models.CharField(max_length=512, blank=True,null=True)
    user_id = models.CharField(max_length=32, blank=True, null=True)
