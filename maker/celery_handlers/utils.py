#coding:utf-8
import re
import os
import commands
import md5
from webviews.models import Packages, Rawfiles, Model
from webviews.models import PbCategory, PbInfo, PbType
from django.core.cache import cache

import logging
logger = logging.getLogger("django")


def get_md5(full_filename):
    f = file(full_filename, 'rb')
    return md5.new(f.read()).hexdigest()


def is_ksyun_server():
    str = commands.getoutput("/sbin/ifconfig")
    return re.search("10.128", str)


def get_mid_by_hash(midhash):
    obj_pkg = cache.get("get_mid_by_hash:%s" % midhash)
    if obj_pkg is None:
        obj_pkg = Packages.objects.filter(idhash=str(midhash))
        cache.set("get_mid_by_hash:%s" % midhash, obj_pkg, 60 * 60 * 24 * 7)
    if len(obj_pkg) == 1:
        logger.debug("find the real mid %d" % (obj_pkg[0].id))
        return obj_pkg[0].id
    else:
        logger.debug("invalid hashid")
        return -1


def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
