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


class PlayEvolutions(models.Model):
    id = models.IntegerField(primary_key=True)
    hash = models.CharField(max_length=255)
    applied_at = models.DateTimeField()
    apply_script = models.TextField(blank=True, null=True)
    revert_script = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    last_problem = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'play_evolutions'


class UcAttributes(models.Model):
    caredearid = models.IntegerField()
    headimg2 = models.CharField(max_length=200, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    idtype = models.CharField(max_length=1, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    headimg = models.CharField(max_length=200, blank=True, null=True)
    realname = models.CharField(max_length=20, blank=True, null=True)
    idno = models.CharField(max_length=50, blank=True, null=True)
    profile = models.CharField(max_length=255, blank=True, null=True)
    issync = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_attributes'


class UcContact(models.Model):
    id = models.BigIntegerField(primary_key=True)
    caredearid = models.IntegerField()
    qq = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_contact'


class UcPassport(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    usermobile = models.CharField(max_length=12, blank=True, null=True)
    third = models.CharField(max_length=50, blank=True, null=True)
    loginpassword = models.CharField(max_length=50, blank=True, null=True)
    paypassword = models.CharField(max_length=50, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=2, blank=True, null=True)
    device = models.CharField(max_length=1, blank=True, null=True)
    lastlogintime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    accode = models.CharField(max_length=20, blank=True, null=True)
    codetime = models.IntegerField(blank=True, null=True)
    brand = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_passport'


class UcScore(models.Model):
    id = models.BigIntegerField(primary_key=True)
    caredearid = models.IntegerField()
    allscore = models.IntegerField(blank=True, null=True)
    nowscore = models.IntegerField(blank=True, null=True)
    scoretypeid = models.IntegerField()
    flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score'


class UcScoreAct(models.Model):
    id = models.BigIntegerField(primary_key=True)
    scoretypeid = models.IntegerField()
    scoremoduleid = models.IntegerField()
    actname = models.CharField(max_length=50, blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)
    acttype = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score_act'


class UcScoreChange(models.Model):
    id = models.IntegerField(primary_key=True)
    scoretypeid = models.IntegerField(blank=True, null=True)
    scoremoduleid = models.IntegerField(blank=True, null=True)
    scoreactid = models.IntegerField(blank=True, null=True)
    scoreruleid = models.IntegerField()
    caredearid = models.IntegerField()
    opttime = models.DateTimeField(blank=True, null=True)
    acttype = models.CharField(max_length=10, blank=True, null=True)
    bisid = models.CharField(max_length=20, blank=True, null=True)
    desp = models.CharField(max_length=200, blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score_change'


class UcScoreLevel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    scoretypeid = models.IntegerField()
    levelname = models.CharField(max_length=50, blank=True, null=True)
    levelvalue = models.IntegerField(blank=True, null=True)
    levelicon = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score_level'


class UcScoreModule(models.Model):
    id = models.BigIntegerField(primary_key=True)
    modulename = models.CharField(max_length=50, blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score_module'


class UcScoreRule(models.Model):
    id = models.BigIntegerField(primary_key=True)
    scoretypeid = models.IntegerField()
    scoremoduleid = models.IntegerField()
    scoreactid = models.IntegerField()
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)
    pointstate = models.CharField(max_length=1, blank=True, null=True)
    pointvalue = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score_rule'


class UcScoreType(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_score_type'


class UcSecurity(models.Model):
    id = models.IntegerField(primary_key=True)
    caredearid = models.IntegerField()
    question = models.CharField(max_length=100, blank=True, null=True)
    ask = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_security'


class UcSession(models.Model):
    id = models.BigIntegerField(primary_key=True)
    caredearid = models.IntegerField()
    ticket = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True)
    lastoperatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_session'


class UcSysAccess(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    ticket = models.CharField(max_length=100, blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_sys_access'


class UcSysSessionconf(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sysid = models.IntegerField()
    isorder = models.CharField(max_length=1, blank=True, null=True)
    lefttime = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_sys_sessionconf'


class UcSysTraffic(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sysid = models.IntegerField()
    intervaltime = models.IntegerField(blank=True, null=True)
    maxtime = models.IntegerField(blank=True, null=True)
    flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uc_sys_traffic'
