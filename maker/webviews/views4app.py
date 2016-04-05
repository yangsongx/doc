#encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

import base64
import json
import logging
import random
import string
import time
import pytz
import datetime
from django.core.mail import send_mail
from Global import QINIU_DOWNLOAD_PREFIX
import sys
from webviews.utils import get_mid_by_hash
from webviews.models import Packages, Rawfiles, Model
from webviews.models import PbCategory, PbInfo, PbType
from market_models import ResourceCategory, ResourceInfo
from django.template import loader
from django.core.cache import cache
from Global import CACHE_DURATION

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger("django")

template_cust_preview_wap = loader.get_template('cust_preview_wap.html')
template_feedback4app = loader.get_template('feedback4app.html')
template_show_navigation4app = loader.get_template('show_navigation4app.html')


def save_feedback(request, fb_src, fb_ver, fb_uid, fb_desp, fb_contacts):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime(
        "%y-%m-%d %H:%M:%S")
    mail_head = '21KE用户意见反馈 --- %s' % fb_src
    mail_body = '来源：%s\n版本：%s\n设备号 : %s\n反馈时间: %s\n客户IP: %s\n联系方式: %s\n问题描述: %s\n' % (
        fb_src, fb_ver, fb_uid, now, ip, fb_contacts, fb_desp)
    logger.debug('\n' + mail_body)
    send_mail(mail_head, mail_body, '21ke@caredear.com',
              ['wecare@caredear.com', 'wx@21ke.com'],
              fail_silently=False)

@xframe_options_exempt
def feedback4app(request):
    res = {}

    try:
        if request.method == 'POST':
            logger.debug('POST method')
            js_data = json.loads(request.body)

            fb_src = js_data['src']
            fb_ver = js_data['ver']
            fb_uid = js_data['uid']
            fb_desp = js_data['desp']
            fb_contacts = js_data['contacts']

            save_feedback(request, fb_src, fb_ver, fb_uid, fb_desp,
                          fb_contacts)
            #return render(request, 'fbdone4app.html')
            res['code'] = '0'
            return HttpResponse(json.dumps(res),
                                content_type="application/json")
        else:
            logger.debug('GET method')

            fb_src = request.GET.get('src')
            fb_ver = request.GET.get('ver')
            fb_uid = request.GET.get('uid')
            context_dict = {'src': fb_src, 'ver': fb_ver, 'uid': fb_uid}
            return HttpResponse(template_feedback4app.render(context_dict))
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)
        res['code'] = '4'  #incorrect request
        return HttpResponse(json.dumps(res), content_type="application/json")


#1007	bootanimation-7
#1006	bootanimation-6
#1005	bootanimation-5
#1004	bootanimation-4
#1003	bootanimation-3
#1002	bootanimation-2
#1001	bootanimation-1
#7	hecard
#6	app
#5	短信铃声
#4	桌面壁纸
#3	锁屏壁纸
#2	开机音乐
#1	来电铃音
class preview_item:
    def __init__(self):
        self.boot1_url = ''
        self.boot2_url = ''
        self.boot3_url = ''
        self.boot4_url = ''
        self.wp_lock_url = ''
        self.wp_head_url = ''
        self.callring_singer = ''
        self.callring_songname = ''
        self.callring_url = ''
        self.bootmusic_singer = ''
        self.bootmusic_songname = ''
        self.bootmusic_url = ''
        self.card_url = ''
        self.applist = []


class app_item:
    def __init__(self):
        self.name = ''
        self.pic = ''
        self.id = 0
        self.url = ''
        self.author = ''
        self.idx = 0


def preview_wap(request, mid_hash, api_ver):
    down_url = 'http://7xio6q.com1.z0.glb.clouddn.com/'
    preview_data = preview_item()
    try:
        mid = get_mid_by_hash(mid_hash)
        if mid != -1:
            objs = cache.get("preview_wap:%d" % mid)
            if objs is None:
                objs = Rawfiles.objects.filter(pac=mid)
                cache.set("preview_wap:%d" % mid, objs, CACHE_DURATION)
            for item in objs:
                if (item.pb_type.id == 7):
                    preview_data.card_url = down_url + item.download_url + "|imageView2/3/w/120/h/200"

                elif (item.pb_type.id == 1001):
                    if (item.pb_info.id == -1):
                        preview_data.boot1_url = down_url + item.download_url + '?imageMogr2/crop/!' + item.crop + '|imageView2/3/w/120/h/200'
                    else:
                        preview_data.boot1_url = item.pb_info.res_file_path + '?imageView2/3/w/120/h/200'

                elif (item.pb_type.id == 1002):
                    if (item.pb_info.id == -1):
                        preview_data.boot2_url = down_url + item.download_url + '?imageMogr2/crop/!' + item.crop + '|imageView2/3/w/120/h/200'
                    else:
                        preview_data.boot2_url = item.pb_info.res_file_path + '?imageView2/3/w/120/h/200'

                elif (item.pb_type.id == 1003):
                    if (item.pb_info.id == -1):
                        preview_data.boot3_url = down_url + item.download_url + '?imageMogr2/crop/!' + item.crop + '|imageView2/3/w/120/h/200'
                    else:
                        preview_data.boot3_url = item.pb_info.res_file_path + '?imageView2/3/w/120/h/200'

                elif (item.pb_type.id == 1004):
                    if (item.pb_info.id == -1):
                        preview_data.boot4_url = down_url + item.download_url + '?imageMogr2/crop/!' + item.crop + '|imageView2/3/w/120/h/200'
                    else:
                        preview_data.boot4_url = item.pb_info.res_file_path + '?imageView2/3/w/120/h/200'

                elif (item.pb_type.id == 3):
                    if (item.pb_info.id == -1):
                        preview_data.wp_lock_url = down_url + item.download_url + '?imageMogr2/crop/!' + item.crop + '|imageView2/3/w/120/h/200'
                    else:
                        preview_data.wp_lock_url = item.pb_info.res_file_path + '?imageView2/3/w/120/h/200'

                elif (item.pb_type.id == 4):
                    if (item.pb_info.id == -1):
                        preview_data.wp_head_url = down_url + item.download_url + '?imageMogr2/crop/!' + item.crop + '|imageView2/3/w/120/h/120'
                    else:
                        preview_data.wp_head_url = item.pb_info.res_file_path + '?imageView2/3/w/120/h/120'

                elif (item.pb_type.id == 2):
                    if (item.pb_info.id == -1):
                        preview_data.bootmusic_songname = item.name
                        preview_data.bootmusic_singer = '自定义铃声'
                        if item.crop:
                            preview_data.bootmusic_url = down_url + item.processed_url
                        else:
                            preview_data.bootmusic_url = down_url + item.download_url
                    else:
                        preview_data.bootmusic_songname = item.pb_info.res_name
                        preview_data.bootmusic_singer = item.pb_info.res_author
                        preview_data.bootmusic_url = item.pb_info.res_file_path

                elif (item.pb_type.id == 1):
                    if (item.pb_info.id == -1):
                        preview_data.callring_songname = item.name
                        preview_data.callring_singer = '自定义铃声'
                        if item.crop:
                            preview_data.callring_url = down_url + item.processed_url
                        else:
                            preview_data.callring_url = down_url + item.download_url
                    else:
                        preview_data.callring_songname = item.pb_info.res_name
                        preview_data.callring_singer = item.pb_info.res_author
                        preview_data.callring_url = item.pb_info.res_file_path

                elif (item.pb_type.id == 6):
                    app_detail = ResourceInfo.objects.using('market').filter(
                        res_pkg__exact=item.name)
                    if len(app_detail) > 0:
                        app = app_item()
                        app.name = app_detail[0].res_name
                        app.pic = app_detail[0].res_icon
                        preview_data.applist.append(app)

        context_dict = {'preview_data': preview_data}
        return HttpResponse(template_cust_preview_wap.render(context_dict))

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        logger.debug('an exception' + info)


def show_navigation(request,api_ver):
    return HttpResponse(template_show_navigation4app.render())
