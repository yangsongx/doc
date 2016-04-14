#coding:utf-8

# [History]
# 2015-07-28 Using multiple watermark feature
# 2015-07-16 Support the draft greeting-card feature
# 2015-07-08 Support the welcome data storing
# 2015-07-02 Let upload token support policy
# 2015-06-30 Try integration with background MQ handler
# 2015-06-24 keep one-single App component currently
#
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import HttpResponse


from webviews.models import Packages, Rawfiles, Model, Membership
from webviews.models import PbCategory, PbInfo, PbType, HelpQA


import base64
import MySQLdb
import commands
import json
import logging
import random
import string
import time
import datetime
import pytz
import httplib, urllib, urllib2
from market_models import ResourceCategory, ResourceInfo
from webviews.utils import get_mid_by_hash
from django.core.cache import cache
import md5

import sys
import os
import re
from Global import MAKERID_SALT, MAKER_VERSION, CACHE_DURATION, MAKER_WEBSITE_URL, QINIU_DOWNLOAD_PREFIX, ERR_MAKER_SUCCESS, ERR_MAKER_NOTFOUND, ERR_MAKER_FILE_MISSING, ERR_MAKER_INVALID_REQ, ERR_MAKER_EXCEPTION
import hashlib

from django.template import loader
from maker import settings

reload(sys)
sys.setdefaultencoding('utf8')

##############################################################
## Django logging. The log files locates at logs/django.log ##
##
## API:
##    logger.debug()
##    logger.info()
##    logger.warning()
##    logger.error()
##    logger.critical()
###############################################################
logger = logging.getLogger("django")
##############################################################/


##############################################################

def maker_index(request):
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, 'main.html')
    else:
        return HttpResponse(template_main.render())


def do_index(request, api_ver):
    #if (request.user_agent.is_pc):
    if True:
        logger.debug(
            "it is PC user , using [%s]" % request.user_agent.browser.family)
        if settings.CAREDEAR_DEBUG_MODE:
            # return render(request, api_ver + '/index.html')
            return render(request, 'home.html')
        else:
            if api_ver == 'v1':
                return HttpResponse(template_index_v1.render())
            elif api_ver == 'v2':
                return HttpResponse(template_index_v2.render())
    else:
        return HttpResponse(
            '<div style="text-align:center;"><img style="width:100%" src="/static/images/inconstruction.jpg"/></div>')


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    sid = ''.join(random.choice(chars) for _ in range(size))
    return sid

def gotoDashboard(request):
    sid = ""
    if ('sid' not in request.COOKIES or  request.COOKIES.get('sid') == ""):
        sid = id_generator()
    else:
        sid = request.COOKIES.get('sid')
        
    context_dict = {
        #FIXME
        #'qrurl': "http://ioniconline.com/%s.jpg"%sid,
        'qrurl': "http://www.ioniconline.com:9999/static/images/21KE.png",
    }

    template = 'cust_launcher.html'
    if settings.CAREDEAR_DEBUG_MODE:
        response =render(request, template, context_dict)
    else:
        response = HttpResponse(template.render(context_dict))

    age = 10*365*24*60*60
    response.set_cookie("sid", sid, expires=age)
    return response

def startWxBot(request, sid):
    data = {}
    rc = os.system("python ./wxctl.py start %s"%sid)
    rc = rc >> 8
    if rc == 0:
        data['rc'] = 0
        data['desp'] = "sucess"
    elif rc == 1:
        data['rc'] = 1
        data['desp'] = "existing"
    else:
        data['rc'] = 2
        data['desp'] = "failed to start"

    return HttpResponse(json.dumps(data), content_type="application/json")


def stopWxBot(request, sid):
    data = {}
    rc = os.system("python ./wxctl.py stop %s"%sid)
    rc = rc >> 8
    if rc == 0:
        data['rc'] = 0
        data['desp'] = "sucess"
    elif rc == 1:
        data['rc'] = 1
        data['desp'] = "not started before"
    else:
        data['rc'] = 2
        data['desp'] = "failed to stop"

    return HttpResponse(json.dumps(data), content_type="application/json")

def restartWxBot(request, sid):
    data = {}
    rc = os.system("python ./wxctl.py restart %s"%sid)
    rc = rc >> 8
    if rc == 0:
        data['rc'] = 0
        data['desp'] = "sucess"
    else:
        data['rc'] = 1
        data['desp'] = "failed to start"

    return HttpResponse(json.dumps(data), content_type="application/json")

def get_md5(full_filename):
    f = file(full_filename, 'rb')
    return md5.new(f.read()).hexdigest()

def getQR(request, sid):
    data = {}
    path1 = "./out/%s/qr.png"%sid
    if os.path.exists(path1):
        val = get_md5(path1)
        os.system("cp %s ./static/images/qr/%s.png"%(path1, val))    
        data['rc'] = 0
        data['url'] = "/static/images/qr/%s.png"%val
    else:
        data['rc'] = 1
        data['url'] = ""
    return HttpResponse(json.dumps(data), content_type="application/json")

def getWxBotLog(request, sid):
    rc = os.system("tail -n 20 out/%s/log.txt > out/%s/log2.txt"%(sid,sid))
    text = ""
    with open("out/%s/log2.txt"%sid) as f:
        for it in f.readlines():
            it = it.replace('\n','</br>')
            text += it

    data = {}
    data['rc'] = 0
    data['desp'] = text
    return HttpResponse(json.dumps(data), content_type="application/json")

def getWxBotStatus(request, sid):
    data = {}
    rc = os.system("python ./wxctl.py status %s"%sid)
    rc = rc >> 8
    if int(rc) == 0:
        data['rc'] = 0
        data['desp'] = "stop"
    elif rc == 1:
        data['rc'] = 1
        data['desp'] = "wait"
    elif rc == 2:
        data['rc'] = 2
        data['desp'] = "login"
    else:
        data['rc'] = rc
        data['desp'] = "failed"

    return HttpResponse(json.dumps(data), content_type="application/json")


def my404(request):
    #return render(request,'error404.html')
    return HttpResponse("our 404")

def my500(request):
    return render(request,'error404.html')
