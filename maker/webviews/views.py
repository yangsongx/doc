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

from qiniu import Auth
from qiniu import put_file

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

from uc_model import UcPassport

import sys
import os
import re
from Global import MAKERID_SALT, MAKER_VERSION, CACHE_DURATION, MAKER_WEBSITE_URL, QINIU_DOWNLOAD_PREFIX, ERR_MAKER_SUCCESS, ERR_MAKER_NOTFOUND, ERR_MAKER_FILE_MISSING, ERR_MAKER_INVALID_REQ, ERR_MAKER_EXCEPTION
import hashlib

from django.core.mail import send_mail
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
if settings.CAREDEAR_DEBUG_MODE is False:
    template_main = loader.get_template('main.html')
    template_cmsupload = loader.get_template('cmsupload.html')

    template_index_v1 = loader.get_template('v1/index.html')
    template_help_v1 = loader.get_template('v1/help.html')
    template_feedback_v1 = loader.get_template('v1/feedback.html')
    template_cust_welcome_v1 = loader.get_template('v1/cust_welcome.html')
    template_cust_model_v1 = loader.get_template('v1/cust_model.html')
    template_cust_app_v1 = loader.get_template('v1/cust_app.html')
    template_cust_submit_v1 = loader.get_template('v1/cust_submit.html')
    template_cust_animation_v1 = loader.get_template('v1/cust_animation.html')
    template_cust_wallpaper_lock_v1 = loader.get_template(
        'v1/cust_wallpaper_lock.html')
    template_cust_wallpaper_head_v1 = loader.get_template(
        'v1/cust_wallpaper_head.html')
    template_cust_ringtone_boot_v1 = loader.get_template(
        'v1/cust_ringtone_boot.html')
    template_cust_ringtone_call_v1 = loader.get_template(
        'v1/cust_ringtone_call.html')
    template_getmypackages_v1 = loader.get_template('v1/getmypackages.html')

    template_index_v2 = loader.get_template('v2/index.html')
    template_help_v2 = loader.get_template('v2/help.html')
    template_feedback_v2 = loader.get_template('v2/feedback.html')
    template_cust_welcome_v2 = loader.get_template('v2/cust_welcome.html')
    template_cust_model_v2 = loader.get_template('v2/cust_model.html')
    template_cust_app_v2 = loader.get_template('v2/cust_app.html')
    template_cust_submit_v2 = loader.get_template('v2/cust_submit.html')
    template_cust_animation_v2 = loader.get_template('v2/cust_animation.html')
    template_cust_wallpaper_lock_v2 = loader.get_template(
        'v2/cust_wallpaper_lock.html')
    template_cust_wallpaper_head_v2 = loader.get_template(
        'v2/cust_wallpaper_head.html')
    template_cust_ringtone_boot_v2 = loader.get_template(
        'v2/cust_ringtone_boot.html')
    template_cust_ringtone_call_v2 = loader.get_template(
        'v2/cust_ringtone_call.html')
    template_getmypackages_v2 = loader.get_template('v2/getmypackages.html')


##############################################################
def pyb_index(request):
    return render(request, 'pyb_index.html')


def set_proxy():
    proxy_handler = urllib2.ProxyHandler({"http": 'http://10.128.16.44:800'})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)


def test_login(request):
    from cas.views import login
    set_proxy()
    print "################# test_login"
    print request
    #return login(request, "http://diy.caredear.com/cas_response", required=False, gateway=False)
    logger.debug("path=" + str(request.path))
    return login(request, "/start", required=False, gateway=False)


def cas_response(tree):
    print "#################### get cas response"
    print tree
    return HttpResponse("OK")

    username = tree[0][0].text
    print "1#################### get cas response"
    user, user_created = User.objects.get_or_create(username=username)
    print "2#################### get cas response"
    profile, created = user.get_profile()
    print "3#################### get cas response"
    profile.email = tree[0][1].text
    print "4#################### get cas response"
    profile.position = tree[0][2].text
    print "5#################### get cas response"
    profile.save()
    return HttpResponse("OK")



# Create your views here.
def cmsupload(request):
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, 'cmsupload.html')
    else:
        return HttpResponse(template_cmsupload.render())


def maker_index(request):
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, 'main.html')
    else:
        return HttpResponse(template_main.render())


def do_index(request, api_ver):
    if (request.user_agent.is_pc):
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


def do_help(request, api_ver):
    ONE_PAGE_OF_FAQ = 10
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    if pageType == 'down':
        curPage += 1
    elif pageType == 'up':
        curPage -= 1
    startPos = (curPage - 1) * ONE_PAGE_OF_FAQ
    endPos = startPos + ONE_PAGE_OF_FAQ

    faq_list_raw = cache.get("cust_help:faqs:%d:%d" % (startPos, endPos))
    if faq_list_raw is None:
        faq_list_raw = HelpQA.objects.all()[startPos:endPos]
        cache.set("cust_help:faqs:%d:%d" % (startPos, endPos), faq_list_raw,
                  CACHE_DURATION)

    #faq_list = enumerate(faq_list_raw)
    if curPage == 1 and allPage == 1:
        allFaqCounts = cache.get("cust_help:faqs:allAppCounts")
        if allFaqCounts is None:
            allFaqCounts = HelpQA.objects.all().count()
            cache.set("cust_help:faqs:allAppCounts", allFaqCounts,
                      CACHE_DURATION)
        if allFaqCounts == 0:
            allPage = 1
        else:
            allPage = allFaqCounts / ONE_PAGE_OF_FAQ
            remainPost = allFaqCounts % ONE_PAGE_OF_FAQ
            if remainPost > 0:
                allPage += 1

    context_dict = {
        'faqs': faq_list_raw,
        'allPage': allPage,
        'curPage': curPage,
        'src': '21KE定制',
        'ver': MAKER_VERSION,
        'uid': str(request.user_agent.device) + '=' + str(
            request.user_agent.browser) + '=' + str(request.user_agent.os)
    }
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, api_ver + '/help.html', context_dict)
    else:
        if api_ver == 'v1':
            return HttpResponse(template_help_v1.render(context_dict))
        elif api_ver == 'v2':
            return HttpResponse(template_help_v2.render(context_dict))


def do_feedback(request, api_ver):
    context_dict = {
        'src': '21KE定制',
        'ver': MAKER_VERSION,
        'uid': str(request.user_agent.device) + '=' + str(
            request.user_agent.browser) + '=' + str(request.user_agent.os)
    }
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, api_ver + '/feedback.html', context_dict)
    else:
        if api_ver == 'v1':
            return HttpResponse(template_feedback_v1.render(context_dict))
        elif api_ver == 'v2':
            return HttpResponse(template_feedback_v2.render(context_dict))


#####################################################################################
def map_pos_in_card_template(templateid, types, data, color, font, size):
    result = ''

    ##### change begin below 2, 3 will changed to 1, 2
    if templateid == 1:
        logger.debug('template-1')
        if types == 'title':
            pos = 'gravity/NorthWest/dx/40/dy/720'
            if data[len(data) - 1] != ':':
                data += ':'
        elif types == 'body':
            pos = 'gravity/NorthWest/dx/40/dy/840'
        else:
            logger.debug('unknow pos')

    elif templateid == 2:
        logger.debug('template-2')
        if types == 'title':
            pos = 'gravity/NorthWest/dx/50/dy/170'
            if data[len(data) - 1] != ':':
                data += ':'
        elif types == 'body':
            pos = 'gravity/NorthWest/dx/50/dy/280'
        else:
            logger.debug('unknow pos')

    elif templateid == 3:
        logger.debug('template-3')
        if types == 'title':
            pos = 'gravity/NorthWest/dx/40/dy/80'
            if data[len(data) - 1] != ':':
                data += ':'
        elif types == 'body':
            pos = 'gravity/NorthWest/dx/40/dy/210'
        else:
            logger.debug('unknow pos')

    elif templateid == 4:
        logger.debug('template-4')
        if types == 'title':
            pos = 'gravity/NorthWest/dx/60/dy/480'
            if data[len(data) - 1] != ':':
                data += ':'
        elif types == 'body':
            pos = 'gravity/NorthWest/dx/40/dy/620'
        else:
            logger.debug('unknow pos')

    else:
        logger.debug('template-unknow')

    urlencode = base64.urlsafe_b64encode(data)
    result = 'text/%s/font/%s/fontsize/%d/fill/%s/%s' \
        %(urlencode, font, size, color, pos)

    logger.debug('the final section url:')
    logger.debug(result)

    return result


#####################################################################################
def map_name_in_card_template(request):
    name = 'tp%02d.jpg' % (request)
    return name


#####################################################################################
def map_sig_pos(sig_length):
    MAXPADDING = 5
    spaces = ''

    for i in range(0, (MAXPADDING - sig_length)):
        spaces += '  '

    # minor modification for longer text case..
    if sig_length >= 4:
        spaces += ' '

    return spaces


#####################################################################################
def get_welcome_url(maker_id):
    url = ''

    # welcome type ID is 7
    obj = Rawfiles.objects.filter(pb_type=PbType(id=7),
                                  pac=Packages(id=maker_id))
    if len(obj) >= 1:
        url = QINIU_DOWNLOAD_PREFIX + obj[0].download_url

    return url


#####################################################################################
# return 1 means need save money, i.e, don't send SMS anymore
def save_money_for_company(phonenum):
    save_money = 0

    mem_val = cache.get(phonenum)
    sec = time.time()

    if mem_val is None:
        cache.set(phonenum, sec, 100)  # don't try send within (1 + 2/3) minutes..
    else:
        save_money = 1

    return save_money


#####################################################################################
def wrap_body_text(templateid, data):
    maxwidth = 12
    rows = 1
    out = ''

    if templateid == 1:
        # happy birthday is longer, so wrap with 8
        maxwidth = 16
        logger.debug('TODO')

    elif templateid == 2:
        logger.debug('TODO')

    elif templateid == 3:
        logger.debug('TODO')

    else:
        logger.warning('template-unknow')

    k = 0
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    for i in range(len(data)):
        match = zhPattern.search(data[i])
        if match:
            if ((k + 1) % maxwidth == 0):
                k = k + 1
            else:
                k = k + 2
        else:
            k = k + 1

        if ((k > 0) and ((k % maxwidth) == 0)):
            out = out + data[i] + '\n  '
        else:
            out = out + data[i]

    return out

#####################################################################################
#Handler for customization web pages


def cust_welcome(request, api_ver):
    if settings.CAREDEAR_DEBUG_MODE:
        return do_cust_welcome(request, 4000, api_ver + '/cust_welcome.html')
    else:
        if api_ver == 'v1':
            return do_cust_welcome(request, 4000, template_cust_welcome_v1)
        elif api_ver == 'v2':
            return do_cust_welcome(request, 4000, template_cust_welcome_v2)


def cust_model(request, api_ver):
    #to be fixed:  Notify the user he/she has a imcomplete make task
    if 'makerid' in request.COOKIES:
        logger.debug("continue the privous maker with %s..." %
                     (request.COOKIES['makerid'], ))
    else:
        logger.debug("this is a fresh model selection page")

    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, api_ver + '/cust_model.html')
    else:
        if api_ver == 'v1':
            return HttpResponse(template_cust_model_v1.render())
        elif api_ver == 'v2':
            return HttpResponse(template_cust_model_v2.render())


ONE_PAGE_OF_IMG_DATA = 4


def do_cust_welcome(request, category_id, template):
    if ('makerid' not in request.COOKIES) or ('model' not in request.COOKIES):
        return HttpResponseRedirect('/' + api_ver + '/maker/cust/model')
    else:
        #count the page number
        try:
            curPage = int(request.GET.get('curPage', '1'))
            allPage = int(request.GET.get('allPage', '1'))
            pageType = str(request.GET.get('pageType', ''))
        except ValueError:
            curPage = 1
            allPage = 1
            pageType = ''
        if pageType == 'down':
            curPage += 1
        elif pageType == 'up':
            curPage -= 1
        startPos = (curPage - 1) * ONE_PAGE_OF_IMG_DATA
        endPos = startPos + ONE_PAGE_OF_IMG_DATA
        model = request.COOKIES['model']
        if model == '3':
            mclass = 'm3'
        else:
            mclass = 'm2c'

        prebuilt_list_raw = cache.get("cust_welcome:prebuilt_list:%d:%d:%d" %
                                      (category_id, startPos, endPos))
        if prebuilt_list_raw is None:
            prebuilt_list_raw = PbInfo.objects.filter(
                res_category_id=category_id)[startPos:endPos]
            cache.set("cust_welcome:prebuilt_list:%d:%d:%d" % (
                category_id, startPos, endPos), prebuilt_list_raw,
                      CACHE_DURATION)

        prebuilt_list = enumerate(prebuilt_list_raw)
        if curPage == 1 and allPage == 1:
            allAppCounts = cache.get(
                "cust_welcome:allAppCounts:%d" % category_id)
            if allAppCounts is None:
                allAppCounts = PbInfo.objects.filter(
                    res_category_id=category_id).count()
                cache.set("cust_welcome:allAppCounts:%d" % category_id,
                          allAppCounts, CACHE_DURATION)
            if allAppCounts == 0:
                allPage = 1
            else:
                allPage = allAppCounts / ONE_PAGE_OF_IMG_DATA
                remainPost = allAppCounts % ONE_PAGE_OF_IMG_DATA
                if remainPost > 0:
                    allPage += 1

        context_dict = {
            'prebuilts': prebuilt_list,
            'allPage': allPage,
            'curPage': curPage,
            'mclass': mclass
        }
        if settings.CAREDEAR_DEBUG_MODE:
            return render(request, template, context_dict)
        else:
            return HttpResponse(template.render(context_dict))


def do_cust_wallpaper(request, category_id, template, page_data_count):
    if ('makerid' not in request.COOKIES) or ('model' not in request.COOKIES):
        return HttpResponseRedirect('/' + api_ver + '/maker/cust/model')
    else:
        #count the page number
        try:
            curPage = int(request.GET.get('curPage', '1'))
            allPage = int(request.GET.get('allPage', '1'))
            pageType = str(request.GET.get('pageType', ''))
        except ValueError:
            curPage = 1
            allPage = 1
            pageType = ''
        if pageType == 'down':
            curPage += 1
        elif pageType == 'up':
            curPage -= 1
        startPos = (curPage - 1) * page_data_count
        endPos = startPos + page_data_count
        model = request.COOKIES['model']
        if model == '3':
            img_width = '720'
            mclass = 'm3'
        else:
            img_width = '480'
            mclass = 'm2c'

        prebuilt_list_raw = cache.get(
            "cust_wallpaper:prebuilt_list:%d:%s:%d:%d" %
            (category_id, model, startPos, endPos))
        if prebuilt_list_raw is None:
            prebuilt_list_raw = PbInfo.objects.filter(
                res_category=category_id,
                extra_info=img_width)[startPos:endPos]
            cache.set("cust_wallpaper:prebuilt_list:%d:%s:%d:%d" % (
                category_id, model, startPos, endPos), prebuilt_list_raw,
                      CACHE_DURATION)

        prebuilt_list = enumerate(prebuilt_list_raw)
        if curPage == 1 and allPage == 1:
            allAppCounts = cache.get(
                "cust_wallpaper:allAppCounts:%d:%s" % (category_id, model))
            if allAppCounts is None:
                allAppCounts = PbInfo.objects.filter(
                    res_category=category_id,
                    extra_info=img_width).count()
                cache.set("cust_wallpaper:allAppCounts:%d:%s" %
                          (category_id, model), allAppCounts, CACHE_DURATION)
            if allAppCounts == 0:
                allPage = 1
            else:
                allPage = allAppCounts / page_data_count
                remainPost = allAppCounts % page_data_count
                if remainPost > 0:
                    allPage += 1

        context_dict = {
            'prebuilts': prebuilt_list,
            'allPage': allPage,
            'curPage': curPage,
            'use_upload': 'True',
            'use_img_crop': 'True',
            'mclass': mclass
        }
        if settings.CAREDEAR_DEBUG_MODE:
            return render(request, template, context_dict)
        else:
            return HttpResponse(template.render(context_dict))


def cust_animation(request, api_ver):
    if settings.CAREDEAR_DEBUG_MODE:
        return do_cust_wallpaper(request, 2000,
                                 api_ver + '/cust_animation.html', 4)
    else:
        if api_ver == 'v1':
            return do_cust_wallpaper(request, 2000, template_cust_animation_v1,
                                     4)
        elif api_ver == 'v2':
            return do_cust_wallpaper(request, 2000, template_cust_animation_v2,
                                     4)


def cust_wallpaper_lock(request, api_ver):
    if settings.CAREDEAR_DEBUG_MODE:
        return do_cust_wallpaper(request, 2000,
                                 api_ver + '/cust_wallpaper_lock.html', 8)
    else:
        if api_ver == 'v1':
            return do_cust_wallpaper(request, 2000,
                                     template_cust_wallpaper_lock_v1, 8)
        elif api_ver == 'v2':
            return do_cust_wallpaper(request, 2000,
                                     template_cust_wallpaper_lock_v2, 8)


def cust_wallpaper_head(request, api_ver):
    if settings.CAREDEAR_DEBUG_MODE:
        return do_cust_wallpaper(request, 3000,
                                 api_ver + '/cust_wallpaper_head.html', 12)
    else:
        if api_ver == 'v1':
            return do_cust_wallpaper(request, 3000,
                                     template_cust_wallpaper_head_v1, 12)
        elif api_ver == 'v2':
            return do_cust_wallpaper(request, 3000,
                                     template_cust_wallpaper_head_v2, 12)


class app_item:
    def __init__(self):
        self.name = ''
        self.pic = ''
        self.id = 0
        self.url = ''
        self.author = ''
        self.idx = 0


class category_item:
    def __init__(self):
        self.isactive = 0
        self.name = ''
        self.tag = ''
        self.applist = []  #app list on this category


ONE_PAGE_OF_DATA = 10


def cust_app(request, api_ver):
    if ('makerid' not in request.COOKIES) or ('model' not in request.COOKIES):
        return HttpResponseRedirect('/' + api_ver + '/maker/cust/model')
    else:
        #count the page number
        try:
            curPage = int(request.GET.get('curPage', '1'))
            allPage = int(request.GET.get('allPage', '1'))
            pageType = str(request.GET.get('pageType', ''))
            curCategory = int(request.GET.get('curCate', '35'))
        except ValueError:
            curPage = 1
            allPage = 1
            pageType = ''
            curCategory = 1
        if pageType == 'down':
            curPage += 1
        elif pageType == 'up':
            curPage -= 1
        startPos = (curPage - 1) * ONE_PAGE_OF_DATA
        endPos = startPos + ONE_PAGE_OF_DATA
        model = request.COOKIES['model']
        if model == '3':
            mclass = 'm3'
        else:
            mclass = 'm2c'

        cate_db_list = cache.get('cust_app:cate_db_list')
        if cate_db_list is None:
            cate_db_list = ResourceCategory.objects.using('market').filter(
                id__lte=38)
            cache.set('cust_app:cate_db_list', cate_db_list, CACHE_DURATION)
        cate_data = []
        for cate_db in cate_db_list:
            cate = category_item()
            cate.name = cate_db.category_name
            cate.tag = cate_db.id

            if cate_db.id == curCategory:
                cate.isactive = 1
            else:
                cate_data.append(cate)
                continue

            app_db_list = cache.get("cust_app:app_db_list:%d:%d:%d" %
                                    (cate_db.id, startPos, endPos))
            if app_db_list is None:
                app_db_list = ResourceInfo.objects.using('market').filter(
                    res_category=cate_db.id).order_by(
                        '-res_recommend_level')[startPos:endPos]
                cache.set("cust_app:app_db_list:%d:%d:%d" % (
                    cate_db.id, startPos, endPos), app_db_list, CACHE_DURATION)
            idx = 0
            for app_db in app_db_list:
                app = app_item()
                app.name = app_db.res_name
                app.pic = app_db.res_icon
                app.url = app_db.res_pkg
                app.id = app_db.id
                app.idx += idx
                idx += 1
                cate.applist.append(app)
            cate_data.append(cate)

            if curPage == 1 and allPage == 1:
                allAppCounts = cache.get(
                    "cust_app:allAppCounts:%d" % cate_db.id)
                if allAppCounts is None:
                    allAppCounts = ResourceInfo.objects.using('market').filter(
                        res_category=cate_db.id).count()
                    cache.set("cust_app:allAppCounts:%d" % cate_db.id,
                              allAppCounts, CACHE_DURATION)
                allPage = allAppCounts / ONE_PAGE_OF_DATA
                remainPost = allAppCounts % ONE_PAGE_OF_DATA
                if remainPost > 0:
                    allPage += 1

        context_dict = {
            'categories': cate_data,
            'curCate': curCategory,
            'allPage': allPage,
            'curPage': curPage,
            'mclass': mclass
        }
        if settings.CAREDEAR_DEBUG_MODE:
            return render(request, api_ver + '/cust_app.html', context_dict)
        else:
            if api_ver == 'v1':
                return HttpResponse(template_cust_app_v1.render(context_dict))
            elif api_ver == 'v2':
                return HttpResponse(template_cust_app_v2.render(context_dict))


def do_cust_ringtone(request, typeid, first_cate, template):
    if ('makerid' not in request.COOKIES) or ('model' not in request.COOKIES):
        return HttpResponseRedirect('/' + api_ver + '/maker/cust/model')
    else:
        try:
            curPage = int(request.GET.get('curPage', '1'))
            allPage = int(request.GET.get('allPage', '1'))
            pageType = str(request.GET.get('pageType', ''))
            curCategory = int(request.GET.get('curCate', first_cate))
        except ValueError:
            curPage = 1
            allPage = 1
            pageType = ''
            curCategory = first_cate
        if pageType == 'down':
            curPage += 1
        elif pageType == 'up':
            curPage -= 1
        startPos = (curPage - 1) * ONE_PAGE_OF_DATA
        endPos = startPos + ONE_PAGE_OF_DATA
        model = request.COOKIES['model']
        if model == '3':
            mclass = 'm3'
        else:
            mclass = 'm2c'

        cate_db_list = cache.get("cust_ringtone:%d:cate_db_list" % typeid)
        if cate_db_list is None:
            cate_db_list = PbCategory.objects.filter(type_id=typeid)
            cache.set("cust_ringtone:%d:cate_db_list" % typeid, cate_db_list,
                      CACHE_DURATION)
        cate_data = []
        for cate_db in cate_db_list:
            cate = category_item()
            cate.name = cate_db.category_name
            cate.tag = cate_db.id

            if cate_db.id == curCategory:
                cate.isactive = 1
            else:
                cate_data.append(cate)
                continue

            app_db_list = cache.get("cust_ringtone:app_db_list:%d:%d:%d:%d" %
                                    (typeid, cate_db.id, startPos, endPos))
            if app_db_list is None:
                app_db_list = PbInfo.objects.filter(
                    res_category=cate_db.id).order_by("-id")[startPos:endPos]
                cache.set("cust_ringtone:app_db_list:%d:%d:%d:%d" % (
                    typeid, cate_db.id, startPos, endPos), app_db_list,
                          CACHE_DURATION)
            idx = 0
            for app_db in app_db_list:
                app = app_item()
                app.name = app_db.res_name
                app.url = app_db.res_file_path
                app.id = app_db.id
                app.idx += idx
                idx += 1
                app.author = app_db.res_author
                cate.applist.append(app)
            cate_data.append(cate)

            if curPage == 1 and allPage == 1:
                allAppCounts = cache.get(
                    "cust_ringtone:allAppCounts:%d:%d" % (typeid, cate_db.id))
                if allAppCounts is None:
                    allAppCounts = PbInfo.objects.filter(
                        res_category=cate_db.id).count()
                    cache.set("cust_ringtone:allAppCounts:%d:%d" % (
                        typeid, cate_db.id), allAppCounts, CACHE_DURATION)

                if allAppCounts == 0:
                    allPage = 1
                else:
                    allPage = allAppCounts / ONE_PAGE_OF_DATA
                    remainPost = allAppCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1

        context_dict = {
            'categories': cate_data,
            'curCate': curCategory,
            'allPage': allPage,
            'curPage': curPage,
            'use_upload': 'True',
            'use_music_crop': 'True',
            'mclass': mclass
        }

        if settings.CAREDEAR_DEBUG_MODE:
            return render(request, template, context_dict)
        else:
            return HttpResponse(template.render(context_dict))


def cust_ringtone_boot(request, api_ver):
    if settings.CAREDEAR_DEBUG_MODE:
        return do_cust_ringtone(request, 2, 1000,
                                api_ver + '/cust_ringtone_boot.html')
    else:
        if api_ver == 'v1':
            return do_cust_ringtone(request, 2, 1000,
                                    template_cust_ringtone_boot_v1)
        elif api_ver == 'v2':
            return do_cust_ringtone(request, 2, 1000,
                                    template_cust_ringtone_boot_v2)


def cust_ringtone_call(request, api_ver):
    if settings.CAREDEAR_DEBUG_MODE:
        return do_cust_ringtone(request, 1, 1,
                                api_ver + '/cust_ringtone_call.html')
    else:
        if api_ver == 'v1':
            return do_cust_ringtone(request, 1, 1,
                                    template_cust_ringtone_call_v1)
        elif api_ver == 'v2':
            return do_cust_ringtone(request, 1, 1,
                                    template_cust_ringtone_call_v2)


def cust_submit(request, api_ver):
    if 'makerid' not in request.COOKIES:
        return HttpResponseRedirect('/' + api_ver + '/maker/cust/model')
    else:
        if request.COOKIES['model'] == '3':
            context_dict = {'mclass': 'm3'}
        else:
            context_dict = {'mclass': 'm2c'}
        if settings.CAREDEAR_DEBUG_MODE:
            return render(request, api_ver + '/cust_submit.html', context_dict)
        else:
            if api_ver == 'v1':
                return HttpResponse(
                    template_cust_submit_v1.render(context_dict))
            elif api_ver == 'v2':
                return HttpResponse(
                    template_cust_submit_v2.render(context_dict))


def autoassociate_caredear_system(request):
    cid = ''

    # NOTE - currently, yz-maker1 is the formal server, we need use
    # root user to across visit uc DB
    try:
        db = MySQLdb.connect(user='root',
                             db='uc',
                             passwd='nanjing@!k',
                             host='yz-mysql1')
        cursor = db.cursor()
        sqlcmd = 'SELECT id FROM uc_passport WHERE usermobile=\'%s\' AND status=1' % (
            request)
        logger.debug('the sql cmd:' + sqlcmd)
        cursor.execute(sqlcmd)
        cid = [row[0] for row in cursor.fetchall()]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)

    return cid


#####################################################################################
def do_begin(request, api_ver):
    model = 'unknow'
    res = {}
    owner = None
    if request.COOKIES != None and "CDMEMBERINFO" in request.COOKIES:
        cdmemberinfo = request.COOKIES['CDMEMBERINFO']
        owner = cdmemberinfo.split('&')[1].split('=')[1]
        print "owner:", owner
    try:
        if request.method == 'POST':
            js_data = json.loads(request.body)
            model = js_data['model']
            comment = js_data['description']

            if comment == '':
                comment = "%s" % datetime.datetime.now(pytz.timezone(
                    'Asia/Shanghai')).strftime("%Y-%m-%d %H:%M")

            obj = Packages(cid=int(owner) if owner else -1, size=0, mod=Model(id=int(model)), \
                       status=0, description=comment, created = datetime.datetime.now())

            obj.save()
            obj.idhash = hashlib.md5(str(obj.id) + MAKERID_SALT).hexdigest()
            obj.save()

            #next will try get the latest ID to caller
            #obj = Packages.objects \
            #      .filter(model=model,description=comment) \
            #      .order_by('-created') # minus here means descend
            #logger.debug( 'totally %d obj found'  %(len(obj)))

            #if len(obj) >= 1:
            #  res['code'] = "0"
            #  res['makerid'] = str(obj[0].id)
            #else:
            #  res['code'] = "12"
            res['code'] = "0"
            res['makerid'] = str(obj.idhash)
        else:
            logger.debug('GET method')
            res['code'] = str(ERR_MAKER_INVALID_REQ)  #invalid req(SHOULD be POST)
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        res['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse(json.dumps(res), content_type="application/json")

    #To be removed: sample code
    #response = render(request,'cust_welcome.html')
    #response.set_cookie('last_visit', datetime.now())
    #return response


    #####################################################################################
def do_uptoken(request, api_ver):
    ret = {}

    # init env of the Qiniu
    access_key = '5haoQZguw4iGPnjUuJnhOGufZMjrQnuSdySzGboj'
    secret_key = 'OADMEtVegAXAhCJBhRSXXeEd_YRYzEPyHwzJDs95'
    q = Auth(access_key, secret_key)

    js_data = json.loads(request.body)
    buck = js_data['bucket']
    exp = js_data['expire']  # FIXME currently, this is not used
    logger.debug('the bucket:%s' % buck)

    contain_policy = 0
    if js_data.has_key('policy'):
        logger.debug('you had policy: %s' % (js_data['policy']))
        contain_policy = 1
    else:
        logger.debug('No policy')

    if js_data.has_key('key'):
        logger.debug('you had key: %s' % (js_data['key']))
    else:
        logger.debug('No key')

    if contain_policy == 1:
        tok = q.upload_token(bucket, exp, js_data['key'], js_data['policy'])
    else:
        tok = q.upload_token(bucket, exp)

    tok = q.upload_token(buck)
    logger.debug('the token:' + tok)

    ret['code'] = '0'
    ret['uptoken'] = tok

    # below 2 lines demo how to upload file after get the token
    #info = put_file(tok, '26778119302e4da727cece429805ab10', '/home/yangsongxiang/abc.jpg')
    #logger.debug( info)

    return HttpResponse(json.dumps(ret))


#apply for token by GET method
def do_uptoken2(request, api_ver):
    ret = {}

    # init env of the Qiniu
    access_key = '5haoQZguw4iGPnjUuJnhOGufZMjrQnuSdySzGboj'
    secret_key = 'OADMEtVegAXAhCJBhRSXXeEd_YRYzEPyHwzJDs95'
    q = Auth(access_key, secret_key)

    #js_data = json.loads(request.body)
    buck = 'cdstatic'
    exp = 30000  # FIXME currently, this is not used
    logger.debug('the bucket2:%s' % buck)

    tok = q.upload_token(buck)
    logger.debug('the token2:' + tok)

    #ret['code'] = '0'
    ret['uptoken'] = tok

    return HttpResponse(json.dumps(ret))


#####################################################################################
def do_upload_all(request, api_ver):
    pass

def update_pack_desp(mid, desp):
    obj = Packages.objects.filter(id=int(mid))
    if len(obj) == 1:
        obj[0].description = desp
        obj[0].save()
        return 0
    else:
        return 5


#####################################################################################
def do_down(request, api_ver):
    ret = {}

    try:
        js_data = json.loads(request.body)
        # Request Json MUST be {"type":0}, NOT {"type": "0"}
        t = js_data['type']

        if t == 0:
            #user directly use the system generated code
            pin = js_data['pinCode']
            logger.debug('pin:' + pin)

            if js_data.has_key('model'):
                cur_model = Model.objects.get(name=js_data['model'])
                obj = Packages.objects.get(pincode=pin, mod=cur_model)
            else:
                obj = Packages.objects.get(pincode=pin)

            logger.debug(
                'the id of your selection:%d,MD5:%s' % (obj.id, obj.md5))
            ret['code'] = '0'
            # the web URL is from Qiniu site
            ret['downloadURL'] = QINIU_DOWNLOAD_PREFIX + obj.md5
            ret['preview'
                ] = MAKER_WEBSITE_URL + 'v1/maker/preview/' + obj.idhash
            ret['welcome'] = get_welcome_url(obj.id)
            ret['description'] = obj.description

        elif t == 1:
            #user use phonenum+phonecode
            ###
            memberobj = Membership.objects.filter(
                target=js_data['target'],
                targetcode=js_data['targetcode'])

            tmp = []
            for it in memberobj:
                item = {}
                obj = Packages.objects.get(id=it.package)
                logger.debug(
                    'the id of your selection:%d,MD5:%s' % (obj.id, obj.md5))
                item['downloadURL'] = QINIU_DOWNLOAD_PREFIX + obj.md5
                item['preview'
                     ] = MAKER_WEBSITE_URL + 'v1/maker/preview/' + obj.idhash
                item['welcome'] = get_welcome_url(obj.id)
                item['description'] = obj.description

                tmp.append(item)

            ret['code'] = '0'
            ret['list'] = tmp

        else:
            ret['code'] = str(ERR_MAKER_INVALID_REQ)  # CDS_ERR_REQ_INCORRECT

    except ObjectDoesNotExist:
        logger.debug('did NOT shoot any meet target')
        ret['code'] = str(ERR_MAKER_FILE_MISSING)

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
def do_finish(request, api_ver):
    ret = {}

    try:
        js_data = json.loads(request.body)
        if js_data.has_key('pinCode'):
            obj = Packages.objects.filter(pincode=js_data['pinCode'])
            if len(obj) > 0:
                count = obj[0].dirty
                if count is None:
                    count = 0

                obj[0].dirty = (count + 1)
                obj[0].save()
        elif js_data.has_key('makerID'):
            mid = get_mid_by_hash(js_data['makerID'])
            obj = Packages.objects.filter(id=mid)
            if len(obj) > 0:
                count = obj[0].dirty
                obj[0].dirty = (count + 1)
                obj[0].save()
        else:
            logger.warning('ignore this update')

        ret['code'] = '0'
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.error('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)

    return HttpResponse(json.dumps(ret))


#####################################################################################
def do_addextraID(request):
    ret = 0

    try:
        js_data = json.loads(request)
        mid = get_mid_by_hash(js_data['makerID'])
        if mid != -1:
            obj = Packages.objects \
                    .get(id=mid)

            obj.target = js_data['target']
            # [2015-07-10] - we will use SMS verify code, so below field
            # is not needed anymore
            #obj.targetcode = js_data['targetcode']

            # Do auto-association with Caredear System, based on phone

            ucobj = UcPassport.objects.using('uc').filter(
                usermobile=js_data['target'])
            if len(ucobj) >= 1:
                obj.cid = ucobj[0].id
                logger.debug('%s ===> %d' % (js_data['target'], obj.cid))

            else:
                logger.debug(
                    'the target is not valid Caredear User, keep CID be -1')
                obj.cid = -1
                ret = 0

            obj.save()
        else:
            ret = 2

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret = 4
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return ret


####################################################################################
# Version-2 of bind phone(support multiple bind phone numbers)
#
# @input: JSON format like:
#          ------------------------------
#          {
#            "makerid":"123",  %<-- un-hashed raw numerical number
#            "targets":"138xx;139xxx"
#  [optional]"email":"xxx@xx.yy"
#          }
#          ------------------------------
# @owner: a String data indicate the CID(CaredearID)
def do_addextraID_v2(request, owner=None):
    ret = 0

    try:
        js_data = json.loads(request)

        mid = js_data['makerid']

        if mid != -1 and js_data['targets']:
            allnums = js_data['targets'].split(';')

            for it in allnums:
                if len(it):
                    logger.debug(
                        "########################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>it:%s"
                        % it)
                    obj = Membership.objects.filter(
                        package=Packages(id=mid),
                        owner=int(owner) if owner else owner,
                        target=it)
                    if len(obj) >= 1:
                        # seems it is existed case, just overwrite for the first match guy...
                        logger.debug(
                            'seems it is existed case, just overwrite for the first match guy')
                        obj[0].modified = datetime.datetime.now()
                        obj[0].save()

                    else:
                        logger.debug(
                            "########################>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>it:%s"
                            % it)
                        # This is a new insertion into membership table
                        newobj = Membership(package = Packages(id=mid), owner=int(owner) if owner else owner, \
                                target=it, modified = datetime.datetime.now())
                        #Next, will do auto-association with Caredear System, based on phone
                        ucobj = UcPassport.objects.using('uc').filter(
                            usermobile=it)
                        if len(ucobj) >= 1:
                            newobj.cid = ucobj[0].id
                            logger.debug('%s ===> %d' % (it, newobj.cid))
                        else:
                            logger.debug(
                                'the target is not valid Caredear User, not touch cid')

                        newobj.save()

                else:
                    logger.info('a blank num, ignore it')

        else:
            ret = ERR_MAKER_FILE_MISSING

        # below code are handling the bind email case
        if js_data.has_key('email') and js_data['email']:
            obj = Membership.objects.filter(
                package=Packages(id=mid),
                owner=int(owner) if owner else owner,
                target=js_data['email'])
            if len(obj) >= 1:
                logger.debug(
                    'seems it is existed case, just overwrite for the first match guy')
                obj[0].modified = datetime.datetime.now()
                obj[0].save()
            else:
                # This is a new insertion into membership table
                newobj = Membership(package = Packages(id=mid), owner=int(owner) if owner else owner, \
                        target = js_data['email'], modified = datetime.datetime.now())
                ucobj = UcPassport.objects.using('uc').filter(
                    email=js_data['email'])
                if len(ucobj) >= 1:
                    newobj.cid = ucobj[0].id
                else:
                    logger.debug(
                        'the email is not valid Caredear User, not touch cid')

                newobj.save()

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret = ERR_MAKER_EXCEPTION
        return ret

    return ret


#####################################################################################
def do_association(request, api_ver):
    ret = {}
    try:
        js_data = json.loads(request.body)
        mid = get_mid_by_hash(js_data['makerID'])
        if mid != -1:
            obj = Packages.objects \
                    .get(id=mid)
            #TODO - maybe I need handle the redudent case in the future
            obj.cid = js_data['cid']
            obj.save()

            ret['code'] = '0'
        else:
            ret['code'] = str(ERR_MAKER_EXCEPTION)

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
def do_verifyphone(request, api_ver):
    ret = {}

    try:
        js_data = json.loads(request.body)
        logger.debug('the JSON data:' + str(js_data))
        #params = urllib.urlencode({'content': 'tom', 'user': js_data['phone']})
        num = random.randint(1000, 9999)
        code = '%04d' % (num)
        smsbody = '21KE验证码:%s' % (code)
        params = json.JSONEncoder().encode(
            {'content': smsbody,
             'user': js_data['phone']})
        headers = {"Content-type": "text/plain"}

        #client = httplib.HTTPConnection("192.168.1.250:9002")
        client = httplib.HTTPConnection("service.caredear.com")
        client.request("POST", "/v1/uc/sendSms", params, headers)
        logger.debug('will get response...')

        response = client.getresponse()
        logger.debug(response.status)

        r = json.loads(response.read())
        logger.debug('status code:')
        logger.debug(r['code'])
        if r['code'] == 0:
            logger.debug('now, need insert it into')
            obj = Packages.objects.filter(target=js_data['phone'])
            logger.debug('totally %d obj found' % (len(obj)))
            if len(obj) >= 1:
                logger.debug('keep going...')
                obj[0].targetcode = code
                obj[0].save()
                ret['code'] = '0'

        logger.debug('closing unused client...')
        client.close()
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
def do_welcome(request, api_ver):
    ret = {}
    ret['code'] = '0'

    font = '5qW35L2T'  # base64 of 'KaiTi'

    redcolor = 'cmVk'  # base64 of 'red'
    bluecolor = 'Ymx1ZQ=='
    blackcolor = 'YmxhY2s='
    defcolor = redcolor  # by default, color is RED

    try:
        js_data = json.loads(request.body)
        logger.debug('the JSON data:' + str(js_data))
        mid = get_mid_by_hash(js_data['makerID'])

        template_id = js_data['template']

        if js_data.has_key('color'):
            logger.debug('using the ' + js_data['color'])
            if js_data['color'] == 'blue':
                defcolor = bluecolor
            elif js_data['color'] == 'black':
                defcolor = blackcolor
        else:
            logger.debug('using default color')

        logger.debug('the final color value:' + defcolor)

        title = js_data['title']
        body = js_data['body']
        sig = js_data['signature']

        name = map_name_in_card_template(int(template_id))

        # title section URL
        title_section = map_pos_in_card_template(int(template_id), 'title',
                                                 title, defcolor, font, 1600)
        sigpos = map_sig_pos(len(sig))
        wrapped_body = wrap_body_text(int(template_id), body)

        tmp_data = '  %s\n    %s%s' % (wrapped_body, sigpos, sig)
        body_section = map_pos_in_card_template(int(template_id), 'body',
                                                tmp_data, defcolor, font, 1400)

        background = PbInfo.objects.get(res_name=name, res_author='21ke')
        logger.debug(' got URL:%s' % (background.res_file_path))

        fullurl = '%s?watermark/3/%s/%s' \
                      %(background.res_file_path, title_section, body_section)
        logger.debug('the full URL:')
        logger.debug(fullurl)
        ret['url'] = fullurl

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
def do_checkpackages(request, api_ver):
    ret = {}

    ret['code'] = '0'

    try:
        js_data = json.loads(request.body)
        logger.debug('the JSON data:' + str(js_data))
        theid = js_data['cid']

        obj = Membership.objects.filter(cid=theid)

        if len(obj) == 0:
            logger.debug('not found any data')
            ret['code'] = str(ERR_MAKER_NOTFOUND)
            return HttpResponse(json.dumps(ret),
                                content_type="application/json")

        tmp = []
        for it in obj:
            item = {}
            makerid = it.package_id

            if js_data.has_key('model'):
                cur_model = Model.objects.get(name=js_data['model'])
                packageobj = Packages.objects.get(id=makerid, mod=cur_model)
            else:
                packageobj = Packages.objects.get(id=makerid)
                model_txt = Model.objects.get(id=packageobj.mod.id)
                if model_txt is None:
                    item['model'] = 'unknown'
                else:
                    item['model'] = model_txt.name

            item['description'] = packageobj.description

            if packageobj.pincode is not None:
                item['pinCode'] = packageobj.pincode

            if packageobj.md5 is not None:
                item['url'] = QINIU_DOWNLOAD_PREFIX + packageobj.md5

            if packageobj.idhash is not None:
                item[
                    'preview'
                ] = MAKER_WEBSITE_URL + api_ver + '/maker/preview/' + packageobj.idhash

            item['welcome'] = get_welcome_url(packageobj.id)

            tmp.append(item)

        ret['list'] = tmp

    except ObjectDoesNotExist:
        logger.debug('did NOT shoot any meet target')
        ret['code'] = str(ERR_MAKER_NOTFOUND)

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])

        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
def get_user_id(cd_mem_info):
    ret = ''
    STR_ACCOUNT = 'account='
    items = cd_mem_info.split('&')
    for i in items:
        pos = i.find(STR_ACCOUNT)
        if (pos != -1):
            ret = i.partition(STR_ACCOUNT)[2]
            break
    return ret


#####################################################################################
def do_getmypackages(request, api_ver):
    context_dict = {
        'src': '21KE定制',
        'ver': MAKER_VERSION,
        'uid': str(request.user_agent.device) + '=' + str(
            request.user_agent.browser) + '=' + str(request.user_agent.os)
    }
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, api_ver + '/getmypackages.html', context_dict)
    else:
        if api_ver == 'v1':
            return HttpResponse(template_getmypackages_v1.render(context_dict))
        elif api_ver == 'v2':
            return HttpResponse(template_getmypackages_v2.render(context_dict))


'''
    if 'CDMEMBERINFO' not in request.COOKIES:
        return test_login(request)
    cd_mem_info = request.COOKIES['CDMEMBERINFO']
    user_id = get_user_id(cd_mem_info)
    ONE_PAGE_OF_PACKAGE = 10
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    if pageType == 'down':
        curPage += 1
    elif pageType == 'up':
        curPage -= 1
    startPos = (curPage - 1) * ONE_PAGE_OF_PACKAGE
    endPos = startPos + ONE_PAGE_OF_PACKAGE

    pkg_list_raw = cache.get("cust_getmypackages:%d:%d" % (startPos, endPos))
    if pkg_list_raw is None:
        pkg_list_raw = Packages.objects.filter(
            cid=int(user_id) if user_id else -100).exclude(
                pincode=None)[startPos:endPos]
        cache.set("cust_getmypackages:%d:%d" % (startPos, endPos),
                  pkg_list_raw, CACHE_DURATION)
    if curPage == 1 and allPage == 1:
        if allPkgCounts is None:
            allPkgCounts = Packages.objects.filter(
                cid=int(user_id) if user_id else -100).exclude(
                    pincode=None).count()
            cache.set("cust_getmypackages:allPkgCounts", allPkgCounts,
                      CACHE_DURATION)
        if allPkgCounts == 0:
            allPage = 1
        else:
            allPage = allPkgCounts / ONE_PAGE_OF_PACKAGE
            remainPost = allPkgCounts % ONE_PAGE_OF_PACKAGE
            if remainPost > 0:
                allPage += 1

    context_dict = {
        'pkgs': pkg_list_raw,
        'allPage': allPage,
        'curPage': curPage,
        'ver': MAKER_VERSION,
        'uid': str(request.user_agent.device) + '=' + str(
            request.user_agent.browser) + '=' + str(request.user_agent.os)
    }
    if settings.CAREDEAR_DEBUG_MODE:
        return render(request, api_ver + '/getmypackages.html', context_dict)
    else:
        return HttpResponse(template_help.render(context_dict))
        if api_ver == 'v1':
            return HttpResponse(template_getmypackages_v1.render())
        elif api_ver == 'v2':
            return HttpResponse(template_getmypackages_v2.render())
'''


def do_getappdetail(request, api_ver):
    ret = {}
    ret['code'] = '0'

    try:
        js_data = json.loads(request.body)
        #logger.debug( 'the JSON data:' + str(js_data))
        pkg = js_data['package']

        obj = cache.get('cust_app:appdetail:%s' % pkg)
        if obj is None:
            obj = ResourceInfo.objects.using('market').filter(
                res_pkg__exact=pkg)
            if len(obj) == 0:
                logger.debug('not found any data')
                ret['code'] = str(ERR_MAKER_NOTFOUND)
                return HttpResponse(json.dumps(ret),
                                    content_type="application/json")
            else:
                cache.set('cust_app:appdetail:%s' % pkg, obj, CACHE_DURATION)

        ret['logo'] = obj[0].res_icon
        ret['name'] = obj[0].res_name
        ret['desp'] = obj[0].res_desp
        ret['ver'] = obj[0].res_version
        ret['down'] = obj[0].res_download_num
        ret['mod'] = str(obj[0].last_modify_time)
        ret['size'] = float('%.2f' % (obj[0].res_length / 1024.0 / 1024.0))
        tmp = re.split(',', obj[0].large_icon_path)
        if (tmp[0]):
            ret['pic0'] = tmp[0]
        if (tmp[1]):
            ret['pic1'] = tmp[1]
        if (tmp[2]):
            ret['pic2'] = tmp[2]
        if (tmp[3]):
            ret['pic3'] = tmp[3]
        if (tmp[4]):
            ret['pic4'] = tmp[4]

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


def getappinfo(request, api_ver, package):
    ret = {}
    ret['code'] = '0'

    try:
        pkg = package

        obj = cache.get('cust_app:appdetail:%s' % pkg)
        if obj is None:
            obj = ResourceInfo.objects.using('market').filter(
                res_pkg__exact=pkg)
            if len(obj) == 0:
                logger.debug('not found any data')
                ret['code'] = str(ERR_MAKER_NOTFOUND)
                return HttpResponse(json.dumps(ret),
                                    content_type="application/json")
            else:
                cache.set('cust_app:appdetail:%s' % pkg, obj, CACHE_DURATION)

        ret['id'] = obj[0].id
        ret['pkg'] = obj[0].res_pkg
        ret['name'] = obj[0].res_name
        ret['version'] = obj[0].res_version
        ret['version_code'] = obj[0].res_version_code
        ret['desp'] = obj[0].res_desp
        ret['icon'] = obj[0].res_icon
        ret['length'] = obj[0].res_length
        ret['res_summary'] = obj[0].res_summary
        ret['large_icon_path'] = obj[0].large_icon_path
        ret['file_path'] = obj[0].res_file_path
        ret['file_hash'] = obj[0].res_file_hash
        ret['price'] = obj[0].res_price
        if ret['price'] is None:
            ret['price'] =""
        ret['download_num'] = obj[0].res_download_num
        ret['recommend_level'] = obj[0].res_recommend_level
        ret['category'] = obj[0].res_category.category_name
        ret['type'] = obj[0].res_type.type_name
        ret['source'] = obj[0].res_source.source_name
        ret['file_size'] = obj[0].file_size
        #ret['last_modify_time'] = obj[0].last_modify_time

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
# This is remove the package(NOT physical file, just logical file ownership)
# for specified user
#
# @input is JSON, like this:
#          ------------------------------
#          {
#            "pinCode":"ab1234",  %<-- The package want to unlink
#            "cid":"100345", %<-- Caredear ID
#          }
#          ------------------------------
def do_unlink(request, api_ver):
    ret = {}
    ret['code'] = '0'

    try:
        js_data = json.loads(request.body)
        pin = js_data['pinCode']

        packageobj = Packages.objects.filter(pincode=pin)
        if len(packageobj) >= 1:
            obj = Membership.objects.filter(
                package=Packages(id=packageobj[0].id),
                cid=js_data['cid'])
            for it in obj:
                it.delete()

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
# @request : the JSON data sent from @do_notify_result
#
def update_membership_table(request):
    ret = 0
    js_data = json.loads(request.body)

    packageobj = Packages.objects.filter(pincode=js_data['code'])
    if len(packageobj) >= 1:
        reqdata = {}
        reqdata['makerid'] = packageobj[0].id
        reqdata['targets'] = js_data['phone']
        reqdata['email'] = js_data['email']
        owner = None
        if request.COOKIES != None and "CDMEMBERINFO" in request.COOKIES:
            cdmemberinfo = request.COOKIES['CDMEMBERINFO']
            owner = cdmemberinfo.split('&')[1].split('=')[1]

        ret = do_addextraID_v2(json.dumps(reqdata), owner)

    return ret


#####################################################################################
def do_notify_result(request, api_ver):
    ret = {}
    # fell free to modify below text
    body = '感谢使用21KE手机定制系统,您的定制码为'
    try:
        js_data = json.loads(request.body)

        phone = js_data['phone']
        code = js_data['code']
        email = js_data['email']

        if (len(phone) == 0 and len(email) == 0):
            ret['code'] = str(ERR_MAKER_INVALID_REQ)
            return HttpResponse(json.dumps(ret))

        # TODO - a workaround to avoid multiple phone
        # currently, only send with the first match phone number

        ###########
        if (len(phone) >= 11):
            if len(phone) > 11:
                logger.debug('workaround to force one-single phone')
                phone = phone[0:11]

            logger.debug('coming->%s %s' % (phone, code))
            if save_money_for_company(phone) == 1:
                logger.debug(' avoid sending too many SMS in short time')
                ret['code'] = 0
            else:
                smscontent = '%s:%s' % (body, code)

                thedata = {'content': smscontent}

                encoded = urllib.urlencode(thedata)
                fullurl = 'http://api.duanxin.cm/?action=send&username=70205948&password=aa320890f7b8fa06ec4ed77a6c8349cf&phone=%s&encode=utf8&%s' % (
                    phone, encoded)
                client = urllib2.Request(fullurl)
                response = urllib2.urlopen(client)
                resdata = response.read()
                if resdata == '100':
                    logger.debug('Successfully send a notify SMS')
                    ret['code'] = 0
                else:
                    ret['code'] = resdata  # provider's code
                ###########

        if (len(email) >= 3):  #tmp code
            mail_head = '21KE手机定制码'
            mail_body = '%s:%s' % (body, code)
            logger.debug(mail_body)
            send_mail(mail_head, mail_body, '21ke@caredear.com', [email],
                      fail_silently=False)
            #Todo: check the return value
            ret['code'] = 0

        # 2015-09-10 need update the newly-created membership
        # FIXME on v2
        #ret['code'] = update_membership_table(request)
        update_membership_table(request)

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps(ret))


#####################################################################################
def compose_all_bind_phone(makerid):
    nums = ''
    obj = Membership.objects.filter(package=Packages(id=makerid))
    if len(obj) >= 1:
        for it in obj:
            nums += it.target
            nums += ';'

    return nums


#####################################################################################
def do_retrieve(request, api_ver):
    ret = {}
    data_list = []

    try:
        js_data = json.loads(request.body)
        logger.debug('the JSON data:' + str(js_data))
        code = js_data['pinCode']

        #Todo : use memcache
        pac_obj = Packages.objects.filter(pincode=js_data['pinCode'])
        if len(pac_obj) > 0:
            raw_obj = Rawfiles.objects.filter(pac=pac_obj[0].id)
            for obj in raw_obj:
                item = []
                if ((obj.pb_type.id == 3) or (obj.pb_type.id == 4) or
                    (obj.pb_type.id >= 1001 and obj.pb_type.id <= 1004)):  #wallpapers
                    if (obj.pb_info.id != -1):  #prebuilt res
                        pbinfo_obj = PbInfo.objects.filter(id=obj.pb_info.id)
                        if len(pbinfo_obj) > 0:
                            download_url = pbinfo_obj[0].res_file_path
                            item.append(obj.pb_type.id)
                            item.append(obj.pb_info.id)
                            item.append(obj.name)
                            item.append(download_url)
                            item.append(obj.suffix)
                            item.append(obj.modified)
                            item.append(obj.crop)
                            item.append(obj.processed_url)
                        else:
                            continue
                    else:
                        item.append(obj.pb_type.id)
                        item.append(obj.pb_info.id)
                        item.append(obj.download_url)
                        if obj.crop:
                            item.append(
                                QINIU_DOWNLOAD_PREFIX + urllib.quote(
                                    obj.download_url.encode("utf-8")) +
                                "?imageMogr2/crop/!" + obj.crop)
                        else:
                            item.append(
                                QINIU_DOWNLOAD_PREFIX + urllib.quote(
                                    obj.download_url.encode("utf-8")))
                        item.append(obj.suffix)
                        item.append(obj.modified)
                        item.append(obj.crop)
                        item.append(obj.processed_url)
                elif (obj.pb_type.id == 6):  #APP
                    market_obj = ResourceInfo.objects.using('market').filter(
                        res_pkg__exact=obj.name)
                    if len(market_obj) > 0:
                        item.append(obj.pb_type.id)
                        item.append(obj.pb_info.id)
                        item.append(obj.name)
                        item.append(market_obj[0].res_icon)
                        item.append(market_obj[0].res_name)
                        item.append(obj.modified)
                        item.append(obj.crop)
                        item.append(obj.processed_url)
                    else:
                        continue
                elif ((obj.pb_type.id == 1) or (obj.pb_type.id == 2) or
                      (obj.pb_type.id == 5)):  #ringtone
                    if (obj.pb_info.id != -1):  #prebuilt res
                        pbinfo_obj = PbInfo.objects.filter(id=obj.pb_info.id)
                        if len(pbinfo_obj) > 0:
                            item.append(obj.pb_type.id)
                            item.append(obj.pb_info.id)
                            item.append(pbinfo_obj[0].res_name)
                            item.append(pbinfo_obj[0].res_file_path)
                            item.append(pbinfo_obj[0].res_author)
                            item.append(obj.modified)
                            item.append(obj.crop)
                            item.append(obj.processed_url)
                        else:
                            continue
                    else:
                        item.append(obj.pb_type.id)
                        item.append(obj.pb_info.id)
                        item.append(obj.name)
                        item.append(QINIU_DOWNLOAD_PREFIX + obj.download_url)
                        item.append(obj.suffix)
                        item.append(obj.modified)
                        item.append(obj.crop)
                        item.append(QINIU_DOWNLOAD_PREFIX + obj.processed_url)
                elif (obj.pb_type.id == 7):  #card
                    item.append(obj.pb_type.id)
                    item.append(obj.pb_info.id)
                    item.append(obj.name)
                    item.append(QINIU_DOWNLOAD_PREFIX + obj.download_url)
                    item.append(obj.suffix)
                    item.append(obj.modified)
                    item.append(obj.crop)
                    item.append(obj.processed_url)

                data_list.append(item)

            ret['data'] = data_list
            ret['makerID'] = pac_obj[0].idhash

            ret['bind'] = compose_all_bind_phone(pac_obj[0].id)

            ret['model'] = pac_obj[0].mod.id
            ret['code'] = 0
        else:
            ret['code'] = str(ERR_MAKER_NOTFOUND)
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        ret['code'] = str(ERR_MAKER_EXCEPTION)  #incorrect request

    return HttpResponse(json.dumps(ret), content_type="application/json")
