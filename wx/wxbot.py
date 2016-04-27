# coding: utf-8
import qrcode
import urllib, urllib2
import cookielib
import datetime
import requests
import xml.dom.minidom
import json
import threading
import time, re, sys, os, random
import multiprocessing
import platform
import logging
from collections import defaultdict
from urlparse import urlparse
from lxml import html
import re
import os
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder
import detect
from PIL import Image
import random
import base64
import md5
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


correctWords = ["臭流氓", "你要教坏小朋友了", "变态的照片", "滚粗，色魔"]
wrongWords = ["照片很健康", "很正常的照片", "good picture"]
switchWords = ["换个话题吧","我们聊聊其他的吧","说说最新的新闻怎么样","有什么好玩的事情"]
_nrWrongWords = len(wrongWords) - 1
_nrCorrectWords = len(correctWords) - 1
_nrSwitchWords =len(switchWords) -1
whitelist = [
              "ChenYang", '流氓兔', "陈洋", "顽童", 
              "杨松祥", "Cannoli", "舊時光","夏天的寒号鸟",
              "陈伟",
            ]
key2Gif = {
    '你好': {"in": ["你好", "在吗"],
           "out": ["你好"]},
    '你是谁': {"in": ["你是谁"],
            "out": ["我是"]},
    '再见': {"in": ["再见", "拜拜"],
           "out": ["再见", "拜拜"]},
    '卖萌': {"in": ["你好可爱"],
           "out": ["人见人爱"]},
    '发照片': {"in": ["发照片", "你的照片", "发张照片"],
            "out": []},
    '发红包之后': {"in": [],
              "out": []},
    '可怜': {"in": [],
           "out": []},
    '哭': {"in": ["哭", "呜呜"],
          "out": ["哭", "呜呜"]},
    '早上好': {"in": ["早上好", "早啊"],
            "out": ["早上好", "早啊"]},
    '晚安': {"in": ["晚安"],
           "out": ["晚安"]},
    '笑': {"in": ["哈哈", "呵呵", "笑脸"],
          "out": ["哈哈", "哈皮"]},
    '谢谢': {"in": ["谢谢", "感谢"],
           "out": ["不客气", "谢谢"]},
    '赞': {"in": ["牛逼", "赞", "厉害"],
          "out": ["赞"]},
}

def isInWhitelist(name):
    logger.debug(name)
    for it in whitelist:
        if it in name:
            logger.debug(it)
            return True

    logger.debug("isInWhitelist returns False")
    return False


gifDic = {}


def load_gif_repo():
    rootdir = "./gif/"
    global gifDic

    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            key = re.sub(r".*/", "", parent)
            if key not in gifDic:
                gifDic[key] = []

            gifDic[key].append(os.path.join(parent, filename))
    print gifDic

def getGifByCate(cate):
    if cate in gifDic:
        idx = random.randint(0, len(gifDic[cate]) - 1)
        return gifDic[cate][idx]
    else:
        return None


def get_gif_per_text(query, resp):
    cate = "主动发起"
    for it in key2Gif:
        for ain in key2Gif[it]['in']:
            if ain in query:
                cate = it
                return cate
        for aout in key2Gif[it]['out']:
            if aout in resp:
                cate = it
                return cate
    return cate


def pick_gif_per_text(query, resp):
    cate = get_gif_per_text(query, resp)
    print cate
    ratio = 0
    if cate == '发照片':
        ratio = 1
    return getGifByCate(cate), ratio, cate


def catchKeyboardInterrupt(fn):
    def wrapper(*args):
        try:
            return fn(*args)
        except KeyboardInterrupt:
            print '\n[*] 强制退出程序'
            logger.debug('[*] 强制退出程序')

    return wrapper


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


class WebWeixin(object):
    #_gtoken = ""
    def __str__(self):
        description = \
        "=========================\n" + \
        "[#] Web Weixin\n" + \
        "[#] Debug Mode: " + str(self.DEBUG) + "\n" + \
        "[#] Uuid: " + self.uuid + "\n" + \
        "[#] Uin: " + str(self.uin) + "\n" + \
        "[#] Sid: " + self.sid + "\n" + \
        "[#] Skey: " + self.skey + "\n" + \
        "[#] DeviceId: " + self.deviceId + "\n" + \
        "[#] PassTicket: " + self.pass_ticket + "\n" + \
        "========================="
        return description

    def __init__(self):
        self.DEBUG = False
        self.uuid = ''
        self.base_uri = ''
        self.redirect_uri = ''
        self.uin = ''
        self.sid = ''
        self.skey = ''
        self.pass_ticket = ''
        self.deviceId = 'e' + repr(random.random())[2:17]
        self.BaseRequest = {}
        self.synckey = ''
        self.SyncKey = []
        self.User = []
        self.MemberList = []
        self.ContactList = []  # 好友
        self.GroupList = []  # 群
        self.GroupMemeberList = []  # 群友
        self.GroupMemeberList2 = {}  # 群2
        self.PublicUsersList = []  # 公众号／服务号
        self.SpecialUsersList = []  # 特殊账号
        self.autoReplyMode = False
        self.syncHost = ''
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        self.interactive = True
        self.autoOpen = False
        self.saveFolder = os.path.join(os.getcwd(), 'saved')
        self.saveSubFolders = {'webwxgeticon': 'icons',
                               'webwxgetheadimg': 'headimgs',
                               'webwxgetmsgimg': 'msgimgs',
                               'webwxgetvideo': 'videos',
                               'webwxgetvoice': 'voices',
                               '_showQRCodeImg2': 'qrcodes'}
        self.appid = 'wx782c26e4c19acffb'
        self.lang = 'zh_CN'
        self.lastCheckTs = time.time()
        self.memberCount = 0
        self.SpecialUsers = [
            'newsapp', 'fmessage', 'filehelper', 'weibo', 'qqmail', 'fmessage',
            'tmessage', 'qmessage', 'qqsync', 'floatbottle', 'lbsapp',
            'shakeapp', 'medianote', 'qqfriend', 'readerapp', 'blogapp',
            'facebookapp', 'masssendapp', 'meishiapp', 'feedsapp', 'voip',
            'blogappweixin', 'weixin', 'brandsessionholder', 'weixinreminder',
            'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c', 'officialaccounts',
            'notification_messages', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c',
            'wxitil', 'userexperience_alarm', 'notification_messages'
        ]
        self.TimeOut = 20  # 同步最短时间间隔（单位：秒）
        self.media_count = -1

        self.cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        opener.addheaders = [('User-agent', self.user_agent)]
        urllib2.install_opener(opener)

    def loadConfig(self, config):
        if config['DEBUG']: self.DEBUG = config['DEBUG']
        if config['autoReplyMode']:
            self.autoReplyMode = config['autoReplyMode']
        if config['user_agent']: self.user_agent = config['user_agent']
        if config['interactive']: self.interactive = config['interactive']
        if config['autoOpen']: self.autoOpen = config['autoOpen']

    def getUUID(self):
        logger.debug("getUUID  ---cy-1")
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid': self.appid,
            'fun': 'new',
            'lang': self.lang,
            '_': int(time.time()),
        }
        data = self._post(url, params, False)
        logger.debug("getUUID  ---cy-2")
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(regx, data)
        if pm:
            code = pm.group(1)
            self.uuid = pm.group(2)
            return code == '200'
        return False

    def genQRCode(self):
        """
        if sys.platform.startswith('win'):
            self._showQRCodeImg()
        else:
            self._str2qr('https://login.weixin.qq.com/l/' + self.uuid)
        """
        self._showQRCodeImg2()
    def _showQRCodeImg(self):
        url = 'https://login.weixin.qq.com/qrcode/' + self.uuid
        params = {'t': 'webwx', '_': int(time.time())}

        data = self._post(url, params, False)
        QRCODE_PATH = self._saveFile('qrcode.jpg', data, '_showQRCodeImg')
        os.startfile(QRCODE_PATH)


    def _get_md5(full_filename):
        f = file(full_filename, 'rb')
        return md5.new(f.read()).hexdigest()


    def _showQRCodeImg2(self):
        sid = sys.argv[1]
        url = 'https://login.weixin.qq.com/qrcode/' + self.uuid
        params = {'t': 'webwx', '_': int(time.time())}

        data = self._post(url, params, False)
        QRCODE_PATH = self._saveFile('qrcode-%s.jpg'%sid, data, '_showQRCodeImg2')

        newPath1 = "out/%s/qrcode.jpg"%sid
        print newPath1
        print ("cp %s %s"%(QRCODE_PATH, newPath1))
        os.system("cp %s %s"%(QRCODE_PATH, newPath1))
        #os.startfile(QRCODE_PATH)


    def waitForLogin(self, tip=1):
        time.sleep(tip)
        url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
            tip, self.uuid, int(time.time()))
        data = self._get(url)
        pm = re.search(r'window.code=(\d+);', data)
        code = pm.group(1)

        if code == '201': return True
        elif code == '200':
            pm = re.search(r'window.redirect_uri="(\S+?)";', data)
            r_uri = pm.group(1) + '&fun=new'
            self.redirect_uri = r_uri
            self.base_uri = r_uri[:r_uri.rfind('/')]
            return True
        elif code == '408':
            self._echo('[登陆超时] \n')
        else:
            self._echo('[登陆异常] \n')
        return False

    def login(self):
        data = self._get(self.redirect_uri)
        doc = xml.dom.minidom.parseString(data)
        root = doc.documentElement

        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.skey = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.sid = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.uin = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.pass_ticket = node.childNodes[0].data

        if '' in (self.skey, self.sid, self.uin, self.pass_ticket):
            return False

        self.BaseRequest = {
            'Uin': int(self.uin),
            'Sid': self.sid,
            'Skey': self.skey,
            'DeviceID': self.deviceId,
        }
        return True

    def webwxinit(self):
        url = self.base_uri + '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (
            self.pass_ticket, self.skey, int(time.time()))
        params = {'BaseRequest': self.BaseRequest}
        dic = self._post(url, params)
        self.SyncKey = dic['SyncKey']
        self.User = dic['User']
        # synckey for synccheck
        self.synckey = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
                                 for keyVal in self.SyncKey['List']])

        return dic['BaseResponse']['Ret'] == 0

    def webwxstatusnotify(self):
        url = self.base_uri + '/webwxstatusnotify?lang=zh_CN&pass_ticket=%s' % (
            self.pass_ticket)
        params = {
            'BaseRequest': self.BaseRequest,
            "Code": 3,
            "FromUserName": self.User['UserName'],
            "ToUserName": self.User['UserName'],
            "ClientMsgId": int(time.time())
        }
        dic = self._post(url, params)

        return dic['BaseResponse']['Ret'] == 0

    #TODO customize the image handling
    def _image_cb(self, fn, name, fromwho):
        print 'Hahaha, this is mine...'
        if isInWhitelist(name) == False:
            return 1  # avoid sending everyone a response...

        # FIXME should use sys to get the working directory?
        imagegood = './gif/good.gif'
        imagebad = './gif/bad.gif'

        img = Image.open(fn)
        rc, ratio = detect.detect(img)
        cur = datetime.datetime.now()
        if rc == True:
            ans = "(%s)鉴黄小兔子：%s" % (
                cur.strftime('%H:%M:%S'),
                correctWords[random.randint(0, _nrCorrectWords)])
            # ans = "鉴黄小兔子：" + correctWords[random.randint(0, _nrCorrectWords)]
        else:
            ans = "(%s)鉴黄小兔子：%s" % (
                cur.strftime('%H:%M:%S'),
                wrongWords[random.randint(0, _nrWrongWords)])
            #ans = "鉴黄小兔子：" + wrongWords[random.randint(0, _nrWrongWords)]
        if self.webwxsendmsg(ans, fromwho):
            logger.debug('自动回复: ' + ans)
        else:
            logger.debug('自动回复失败')

        # FIXME - should combine this with above txt msg?
        if rc == True:
            self.sendImg(fromwho, imagebad)
        else:
            self.sendImg(fromwho, imagegood)

        return 0

    def webwxgetcontact(self):
        SpecialUsers = self.SpecialUsers
        print self.base_uri
        url = self.base_uri + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (
            self.pass_ticket, self.skey, int(time.time()))
        dic = self._post(url, {})

        self.MemberCount = dic['MemberCount']
        self.MemberList = dic['MemberList']
        ContactList = self.MemberList[:]
        GroupList = self.GroupList[:]
        PublicUsersList = self.PublicUsersList[:]
        SpecialUsersList = self.SpecialUsersList[:]

        for i in xrange(len(ContactList) - 1, -1, -1):
            Contact = ContactList[i]
            if Contact['VerifyFlag'] & 8 != 0:  # 公众号/服务号
                ContactList.remove(Contact)
                self.PublicUsersList.append(Contact)
            elif Contact['UserName'] in SpecialUsers:  # 特殊账号
                ContactList.remove(Contact)
                self.SpecialUsersList.append(Contact)
            elif Contact['UserName'].find('@@') != -1:  # 群聊
                ContactList.remove(Contact)
                self.GroupList.append(Contact)
            elif Contact['UserName'] == self.User['UserName']:  # 自己
                ContactList.remove(Contact)
        self.ContactList = ContactList

        return True

    def webwxbatchgetcontact(self):
        url = self.base_uri + '/webwxbatchgetcontact?type=ex&r=%s&pass_ticket=%s' % (
            int(time.time()), self.pass_ticket)
        params = {
            'BaseRequest': self.BaseRequest,
            "Count": len(self.GroupList),
            "List": [{"UserName": g['UserName'],
                      "EncryChatRoomId": ""} for g in self.GroupList]
        }
        dic = self._post(url, params)

        # blabla ...
        ContactList = dic['ContactList']
        ContactCount = dic['Count']
        self.GroupList = ContactList

        for i in xrange(len(ContactList) - 1, -1, -1):
            Contact = ContactList[i]
            MemberList = Contact['MemberList']
            for member in MemberList:
                self.GroupMemeberList.append(member)

        #logger.debug(self.ContactList)
        #logger.debug(self.GroupList)
        #logger.debug(self.GroupMemeberList)
        return True

    def getNameById(self, id):
        url = self.base_uri + '/webwxbatchgetcontact?type=ex&r=%s&pass_ticket=%s' % (
            int(time.time()), self.pass_ticket)
        params = {
            'BaseRequest': self.BaseRequest,
            "Count": 1,
            "List": [{"UserName": id,
                      "EncryChatRoomId": ""}]
        }
        dic = self._post(url, params)

        # blabla ...
        return dic['ContactList']

    def testsynccheck(self):
        SyncHost = [
            'webpush.weixin.qq.com',
            'webpush2.weixin.qq.com',
            'webpush.wechat.com',
            'webpush1.wechat.com',
            'webpush2.wechat.com',
            'webpush1.wechatapp.com',
            # 'webpush.wechatapp.com'
        ]
        for host in SyncHost:
            self.syncHost = host
            [retcode, selector] = self.synccheck()
            if retcode == '0': return True
        return False

    def synccheck(self):
        params = {
            'r': int(time.time()),
            'sid': self.sid,
            'uin': self.uin,
            'skey': self.skey,
            'deviceid': self.deviceId,
            'synckey': self.synckey,
            '_': int(time.time()),
        }
        url = 'https://' + self.syncHost + '/cgi-bin/mmwebwx-bin/synccheck?' + urllib.urlencode(
            params)
        try:
            data = self._get(url)
            pm = re.search(
                r'window.synccheck={retcode:"(\d+)",selector:"(\d+)"}', data)
            retcode = pm.group(1)
            selector = pm.group(2)
            return [retcode, selector]
        except:
            return [9999, 1000]

    def webwxsync(self):
        url = self.base_uri + '/webwxsync?sid=%s&skey=%s&pass_ticket=%s' % (
            self.sid, self.skey, self.pass_ticket)
        params = {
            'BaseRequest': self.BaseRequest,
            'SyncKey': self.SyncKey,
            'rr': ~int(time.time())
        }
        dic = self._post(url, params)
        if self.DEBUG:
            print json.dumps(dic, indent=4)
            logger.debug(json.dumps(dic, indent=4))

        if dic is not None and dic['BaseResponse']['Ret'] == 0:
            self.SyncKey = dic['SyncKey']
            self.synckey = '|'.join([str(keyVal['Key']) + '_' + str(keyVal[
                'Val']) for keyVal in self.SyncKey['List']])
        return dic

    def webwxsendmsg(self, word, to='filehelper'):
        logger.debug("CY enter webwxsendmsg")
        url = self.base_uri + '/webwxsendmsg?pass_ticket=%s' % (
            self.pass_ticket)
        clientMsgId = str(int(time.time() * 1000)) + str(random.random())[:5].replace('.', '')
        params = {
            'BaseRequest': self.BaseRequest,
            'Msg': {
                "Type": 1,
                "Content": self._transcoding(word),
                "FromUserName": self.User['UserName'],
                "ToUserName": to,
                "LocalID": clientMsgId,
                "ClientMsgId": clientMsgId
            }
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii=False).encode('utf8')
        r = requests.post(url, data=data, headers=headers)
        dic = r.json()

        logger.debug(dic)
        return dic['BaseResponse']['Ret'] == 0

    def webwxuploadmedia(self, image_name):
        print "CY enter webwxuploadmedia", image_name
        url = 'https://file.wx.qq.com/cgi-bin/mmwebwx-bin/webwxuploadmedia?f=json'
        # 计数器
        self.media_count = self.media_count + 1
        # 文件名
        file_name = image_name
        # MIME格式
        # mime_type = application/pdf, image/jpeg, image/png, etc.
        mime_type = mimetypes.guess_type(image_name, strict=False)[0]
        # 微信识别的文档格式，微信服务器应该只支持两种类型的格式。pic和doc
        # pic格式，直接显示。doc格式则显示为文件。
        #media_type = 'pic' if mime_type.split('/')[0] == 'image' else 'doc'
        media_type = 'pic' if not image_name[-4:] == '.gif' else 'doc'
        print "CY media_type:", media_type
        # 上一次修改日期
        lastModifieDate = 'Thu Mar 17 2016 00:55:10 GMT+0800 (CST)'
        # 文件大小
        file_size = os.path.getsize(file_name)
        # PassTicket
        pass_ticket = self.pass_ticket
        # clientMediaId
        client_media_id = str(int(time.time() * 1000)) + str(random.random(
        ))[:5].replace('.', '')
        # webwx_data_ticket
        webwx_data_ticket = ''
        for item in self.cookie:
            if item.name == 'webwx_data_ticket':
                webwx_data_ticket = item.value
                break
        if (webwx_data_ticket == ''):
            return "None Fuck Cookie"

        uploadmediarequest = json.dumps(
            {
                "BaseRequest": self.BaseRequest,
                "ClientMediaId": client_media_id,
                "TotalLen": file_size,
                "StartPos": 0,
                "DataLen": file_size,
                "MediaType": 4
            },
            ensure_ascii=False).encode('utf8')

        multipart_encoder = MultipartEncoder(
            fields={
                'id': 'WU_FILE_' + str(self.media_count),
                'name': file_name,
                'type': mime_type,
                'lastModifieDate': lastModifieDate,
                'size': str(file_size),
                'mediatype': media_type,
                'uploadmediarequest': uploadmediarequest,
                'webwx_data_ticket': webwx_data_ticket,
                'pass_ticket': pass_ticket,
                'filename': (file_name, open(file_name, 'rb'), mime_type.split(
                    '/')[1])
            },
            boundary=
            '-----------------------------1575017231431605357584454111')

        headers = {
            'Host': 'file.wx.qq.com',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://wx2.qq.com/',
            'Content-Type': multipart_encoder.content_type,
            'Origin': 'https://wx2.qq.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        try:
            r = requests.post(url, data=multipart_encoder, headers=headers)
            response_json = r.json()

            print "CY ==2", response_json
            if response_json['BaseResponse']['Ret'] == 0:
                return response_json
        except:
            print "skip exception"
        return None

    def webwxsendmsgimg(self, user_id, media_id, file_name):
        print "CY enter webwxsendmsgimg"
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsgimg?fun=async&f=json&pass_ticket=%s' % self.pass_ticket
        clientMsgId = str(int(time.time() * 1000)) + str(random.random(
        ))[:5].replace('.', '')
        data_json = {
            "BaseRequest": self.BaseRequest,
            "Msg": {
                "Type": 3,
                "MediaId": media_id,
                "FromUserName": self.User['UserName'],
                "ToUserName": user_id,
                "LocalID": clientMsgId,
                "ClientMsgId": clientMsgId
            }
        }

        if file_name[-4:] == '.gif':
            url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendemoticon?fun=sys&f=json&pass_ticket=%s' % self.pass_ticket
            data_json['Msg']['Type'] = 47
            data_json['Msg']['EmojiFlag'] = 2

        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(data_json, ensure_ascii=False).encode('utf8')
        print "dump data:", data
        r = requests.post(url, data=data, headers=headers)
        dic = r.json()
        print "resp:", dic
        return dic['BaseResponse']['Ret'] == 0

    def _write_file_within_threads(self, fn, data, name, fromwho, cb):
        cur = datetime.datetime.now()
        logger.debug('%s [threading]Saving: %s' %
                     (fn, cur.strftime('%H:%M:%S')))
        try:
            f = open(fn, 'wb')
            f.write(data)
            f.close()
        except:
            logger.error('%s||%s' % (sys.exc_info()[0], sys.exc_info()[1]))

        #time.sleep(3)  # fake time-consuming condition
        if cb != None:
            print 'try trigger the callback...'
            cb(fn, name, fromwho)

        cur = datetime.datetime.now()
        logger.debug('%s [threading]finished saving: %s' %
                     (fn, cur.strftime('%H:%M:%S')))
        return fn

    #ysx code chaning...
    #Adding an extra info @fromwho, to let background thread be able to send response
    def _saveFile(self,
                  filename,
                  data,
                  api=None,
                  name=None,
                  fromwho=None,
                  cb=None):
        fn = filename
        if self.saveSubFolders[api]:
            dirName = os.path.join(self.saveFolder, self.saveSubFolders[api])
            if not os.path.exists(dirName):
                os.makedirs(dirName)
            fn = os.path.join(dirName, filename)
            cur = datetime.datetime.now()
            logger.debug('%s [main]Saved file: %s' %
                         (fn, cur.strftime('%H:%M:%S')))
            #changed by ysx - try save file within threads......
            saveThd = threading.Thread(target = self._write_file_within_threads,\
              args = (fn, data, name, fromwho, cb))
            #FIXME - when set with True, testing result seems not good...
            saveThd.setDaemon(False)
            saveThd.start()
            cur = datetime.datetime.now()
            logger.debug('%s [main]return %s file saving' %
                         (fn, cur.strftime('%H:%M:%S')))
        return fn

    def webwxgeticon(self, id):
        url = self.base_uri + '/webwxgeticon?username=%s&skey=%s' % (id,
                                                                     self.skey)
        data = self._get(url)
        fn = 'img_' + id + '.jpg'
        return self._saveFile(fn, data, 'webwxgeticon')

    def webwxgetheadimg(self, id):
        url = self.base_uri + '/webwxgetheadimg?username=%s&skey=%s' % (
            id, self.skey)
        data = self._get(url)
        fn = 'img_' + id + '.jpg'
        return self._saveFile(fn, data, 'webwxgetheadimg')

    def webwxgetmsgimg(self, msgid, name, fromwho, img_cb):
        url = self.base_uri + '/webwxgetmsgimg?MsgID=%s&skey=%s' % (msgid,
                                                                    self.skey)
        data = self._get(url)
        fn = 'img_' + msgid + '.jpg'
        return self._saveFile(fn, data, 'webwxgetmsgimg', name, fromwho,
                              img_cb)

    #This is an async function, for handling the image case...
    #TODO - function naming convention need be changed to a brand-specific one...
    def foo_halding_img_async(self, msgid, fromwho):
        url = self.base_uri + '/webwxgetmsgimg?MsgID=%s&skey=%s' % (msgid,
                                                                    self.skey)
        data = self._get(url)
        fn = 'img_' + msgid + '.jpg'
        return self._saveFile(fn, data, 'webwxgetmsgimg')

    # Not work now for weixin haven't support this API
    def webwxgetvideo(self, msgid):
        url = self.base_uri + '/webwxgetvideo?msgid=%s&skey=%s' % (msgid,
                                                                   self.skey)
        data = self._get(url, api='webwxgetvideo')
        fn = 'video_' + msgid + '.mp4'
        return self._saveFile(fn, data, 'webwxgetvideo')

    def webwxgetvoice(self, msgid):
        url = self.base_uri + '/webwxgetvoice?msgid=%s&skey=%s' % (msgid,
                                                                   self.skey)
        data = self._get(url)
        fn = 'voice_' + msgid + '.mp3'
        return self._saveFile(fn, data, 'webwxgetvoice')

    def getGroupMemberList(self, id):
        if id in self.GroupMemeberList2:
            return self.GroupMemeberList2[id]
        else:
            return None

    def getGroupName(self, id):
        logger.debug("Call getGroupName %s" % id)

        name = '未知群'
        for member in self.GroupList:
            if member['UserName'] == id:
                name = member['NickName']
        if name == '未知群':
            # 现有群里面查不到
            GroupList = self.getNameById(id)
            for group in GroupList:
                self.GroupList.append(group)
                if group['UserName'] == id:
                    name = group['NickName']
                    MemberList = group['MemberList']
                    self.GroupMemeberList2[id] = []
                    for member in MemberList:
                        self.GroupMemeberList2[id].append(member)
                        self.GroupMemeberList.append(member)
        #logger.debug(self.GroupMemeberList)
        #logger.debug(name)
        return name

    def getUserRemarkName(self, id):
        name = '未知群' if id[:2] == '@@' else '陌生人'
        if id == self.User['UserName']: return self.User['NickName']  # 自己

        if id[:2] == '@@':
            # 群
            name = self.getGroupName(id)
        else:
            # 特殊账号
            for member in self.SpecialUsersList:
                if member['UserName'] == id:
                    name = member['RemarkName'] if member[
                        'RemarkName'] else member['NickName']

            # 公众号或服务号
            for member in self.PublicUsersList:
                if member['UserName'] == id:
                    name = member['RemarkName'] if member[
                        'RemarkName'] else member['NickName']

            # 直接联系人
            for member in self.ContactList:
                if member['UserName'] == id:
                    name = member['RemarkName'] if member[
                        'RemarkName'] else member['NickName']
            # 群友
            for member in self.GroupMemeberList:
                if member['UserName'] == id:
                    name = member['DisplayName'] if member[
                        'DisplayName'] else member['NickName']

        if name == '未知群' or name == '陌生人': logger.debug(id)
        return name

    def getUSerID(self, name):
        for member in self.MemberList:
            if name == member['RemarkName'] or name == member['NickName']:
                return member['UserName']
        return None

    def _showMsg(self, message):

        srcName = None
        dstName = None
        groupName = None
        content = None

        msg = message
        #logger.debug(msg)

        if msg['raw_msg']:
            srcName = self.getUserRemarkName(msg['raw_msg']['FromUserName'])
            dstName = self.getUserRemarkName(msg['raw_msg']['ToUserName'])
            content = msg['raw_msg']['Content'].replace('&lt;', '<').replace(
                '&gt;', '>')
            message_id = msg['raw_msg']['MsgId']

            if content.find(
                    'http://weixin.qq.com/cgi-bin/redirectforward?args=') != -1:
                # 地理位置消息
                data = self._get(content).decode('gbk').encode('utf-8')
                pos = self._searchContent('title', data, 'xml')
                tree = html.fromstring(self._get(content))
                url = tree.xpath('//html/body/div/img')[0].attrib['src']

                for item in urlparse(url).query.split('&'):
                    if item.split('=')[0] == 'center':
                        loc = item.split('=')[-1:]

                content = '%s 发送了一个 位置消息 - 我在 [%s](%s) @ %s]' % (srcName, pos,
                                                                 url, loc)

            if msg['raw_msg']['ToUserName'] == 'filehelper':
                # 文件传输助手
                dstName = '文件传输助手'

            if msg['raw_msg']['FromUserName'][:2] == '@@':
                # 接收到来自群的消息
                if re.search(":<br/>", content, re.IGNORECASE):
                    [people, content] = content.split(':<br/>')
                    groupName = srcName
                    srcName = self.getUserRemarkName(people)
                    dstName = 'GROUP'
                else:
                    groupName = srcName
                    srcName = 'SYSTEM'
            elif msg['raw_msg']['ToUserName'][:2] == '@@':
                # 自己发给群的消息
                groupName = dstName
                dstName = 'GROUP'

            # 收到了红包
            if content == '收到红包，请在手机上查看': msg['message'] = content

            # 指定了消息内容
            if 'message' in msg.keys(): content = msg['message']

        if groupName != None:
            print '%s |%s| %s -> %s: %s' % (message_id, groupName.strip(),
                                            srcName.strip(), dstName.strip(),
                                            content.replace('<br/>', '\n'))
            logger.debug('%s |%s| %s -> %s: %s' %
                         (message_id, groupName.strip(), srcName.strip(),
                          dstName.strip(), content.replace('<br/>', '\n')))
        else:
            print '%s %s -> %s: %s' % (message_id, srcName.strip(),
                                       dstName.strip(), content.replace(
                                           '<br/>', '\n'))
            logger.debug('%s %s -> %s: %s' %
                         (message_id, srcName.strip(), dstName.strip(),
                          content.replace('<br/>', '\n')))

        return srcName, dstName

    def handleMsg(self, r):
        for msg in r['AddMsgList']:
            print '[*] 你有新的消息，请注意查收'
            logger.debug('[*] 你有新的消息，请注意查收')

            if self.DEBUG:
                fn = 'msg' + str(int(random.random() * 1000)) + '.json'
                with open(fn, 'w') as f:
                    f.write(json.dumps(msg))
                print '[*] 该消息已储存到文件: ' + fn
                logger.debug('[*] 该消息已储存到文件: %s' % (fn))

            msgType = msg['MsgType']
            name = self.getUserRemarkName(msg['FromUserName'])
            content = msg['Content'].replace('&lt;', '<').replace('&gt;', '>')
            msgid = msg['MsgId']

            if msgType == 1:
                raw_msg = {'raw_msg': msg}
                self._showMsg(raw_msg)
                logger.debug(raw_msg)

                if isInWhitelist(name) == False:
                    break

                    #				mlist = []
                    #				mlist = self.getGroupMemberList(msg['FromUserName'])
                    #				for it in mlist:
                    #					logger.debug("%s, %s" %(it['UserName'],(it['NickName'] )))

                if self.autoReplyMode:
                    #if True:
                    logger.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    logger.debug(content)
                    #if (len(content) < 200) and (content.startswith('#') or content.startswith('@')):
                    '''
                    if (len(content) < 200) and (
                        (content.startswith('@') and content.find('＃') != -1 or
                         content.find('#') != -1 or content.find('兔') != -1) or
                        (not content.startswith('@'))):
                    '''
                    if len(content) < 200:
                        ans = self._smart(content, msg['FromUserName'])
                        ans = ans.replace("米小兔", "流氓兔")
                        ans = ans.replace("米兔", "流氓兔")
                        ans = ans.replace("图灵机器人", "")
                        ans = ans.replace("机器岛", "世界")
                        ans = ans.replace("你说的内容我暂时还没法理解", "哦")
                    else:
                        ans = switchWords[random.randint(0, _nrSwitchWords)]

                    if True:
                        logger.debug(type(ans))
                        if self.webwxsendmsg(ans, msg['FromUserName']):
                            #print '自动回复: '+ans
                            logger.debug('自动回复: ' + ans)
                        else:
                            #print '自动回复失败'
                            logger.debug('自动回复失败')
                         
                        break
                        gifFile, ratio, cate = pick_gif_per_text(content, ans)
                        ifShow = 1
                        if ratio < 1:
                            ifShow = random.randint(0, 1)

                        if ifShow > 0:
                            if gifFile is not None:
                                logger.debug(gifFile)
                                self.sendImg(msg['FromUserName'], gifFile)

#						for it in mlist:
#							self.webwxsendmsg("%s邀请您参加游戏"%name, it['UserName'])

#logger.debug(self.MemberList)
#logger.debug(self.ContactList)
#logger.debug(self.GroupList)
#logger.debug(self.GroupMemeberList)
#self.sendMsgToAll("test")
                    else:
                        gifFile, ratio, cate = pick_gif_per_text(content, "")
                        ifShow = 1
                        if ratio < 1:
                            ifShow = random.randint(0, 1)
                        #if cate == '主动发起':
                        #	ifShow = False

                        if ifShow > 0:
                            if gifFile is not None:
                                self.sendImg(msg['FromUserName'], gifFile)

            elif msgType == 3:
                break
                image = self.webwxgetmsgimg(msgid, name, \
                  msg['FromUserName'], self._image_cb)
                raw_msg = {'raw_msg': msg,
                           'message': '%s 发送了一张图片: %s' % (name, image)}
                self._showMsg(raw_msg)
                if isInWhitelist(name) == True:
                    cur = datetime.datetime.now()
                    fmt = '(%s) handling req, be patient...' % (
                        cur.strftime('%H:%M:%S'))
                    self.webwxsendmsg(fmt, msg['FromUserName'])

#		self._safe_open(image)
            elif msgType == 34:
                if isInWhitelist(name) == False:
                    logger.debug("Skip audio msg")
                    break
                #print "skip Audio msg"
                voice = self.webwxgetvoice(msgid)
                raw_msg = {'raw_msg': msg,
                           'message': '%s 发了一段语音: %s' % (name, voice)}
                src, dest = self._showMsg(raw_msg)
                logger.debug(src)
                logger.debug(dest)
                asr = self._audio2Text(voice)
                logger.debug(self.getUserRemarkName(msg['ToUserName']))
                if asr != "":
                    resp = "[微信助手] %s说: %s" % (src, asr)
                else:
                    resp = "[微信助手] 无法识别%s刚刚的语音消息，暂时只支持普通话" % src
                self.webwxsendmsg(resp, msg['FromUserName'])

                #self._safe_open(voice)
            elif msgType == 42:
                break
                info = msg['RecommendInfo']
                print '%s 发送了一张名片:' % name
                print '========================='
                print '= 昵称: %s' % info['NickName']
                print '= 微信号: %s' % info['Alias']
                print '= 地区: %s %s' % (info['Province'], info['City'])
                print '= 性别: %s' % ['未知', '男', '女'][info['Sex']]
                print '========================='
                raw_msg = {'raw_msg': msg,
                           'message':
                           '%s 发送了一张名片: %s' % (name.strip(), json.dumps(info))}
                self._showMsg(raw_msg)
            elif msgType == 47:
                break
                url = self._searchContent('cdnurl', content)
                raw_msg = {'raw_msg': msg,
                           'message': '%s 发了一个动画表情，点击下面链接查看: %s' % (name, url)}
                self._showMsg(raw_msg)
                self._safe_open(url)
            elif msgType == 49:
                break
                appMsgType = defaultdict(lambda: "")
                appMsgType.update({5: '链接', 3: '音乐', 7: '微博'})
                print '%s 分享了一个%s:' % (name, appMsgType[msg['AppMsgType']])
                print '========================='
                print '= 标题: %s' % msg['FileName']
                print '= 描述: %s' % self._searchContent('des', content, 'xml')
                print '= 链接: %s' % msg['Url']
                print '= 来自: %s' % self._searchContent('appname', content,
                                                       'xml')
                print '========================='
                card = {
                    'title': msg['FileName'],
                    'description': self._searchContent('des', content, 'xml'),
                    'url': msg['Url'],
                    'appname': self._searchContent('appname', content, 'xml')
                }
                raw_msg = {'raw_msg': msg,
                           'message': '%s 分享了一个%s: %s' %
                           (name, appMsgType[msg['AppMsgType']],
                            json.dumps(card))}
                self._showMsg(raw_msg)
            elif msgType == 51:
                raw_msg = {'raw_msg': msg, 'message': '[*] 成功获取联系人信息'}
                self._showMsg(raw_msg)
            elif msgType == 62:
                print "skip Video msg"
                #video = self.webwxgetvideo(msgid)
                #raw_msg = { 'raw_msg': msg, 'message': '%s 发了一段小视频: %s' % (name, video) }
                #self._showMsg(raw_msg)
                #self._safe_open(video)
            elif msgType == 10002:
                break
                raw_msg = {'raw_msg': msg, 'message': '%s 撤回了一条消息' % name}
                self._showMsg(raw_msg)
            else:
                logger.debug('[*] 该消息类型为: %d，可能是表情，图片, 链接或红包: %s' %
                             (msg['MsgType'], json.dumps(msg)))
                raw_msg = {'raw_msg': msg,
                           'message':
                           '[*] 该消息类型为: %d，可能是表情，图片, 链接或红包' % msg['MsgType']}
                self._showMsg(raw_msg)

    def listenMsgMode(self):
        print '[*] 进入消息监听模式 ... 成功'
        logger.debug('[*] 进入消息监听模式 ... 成功')
        self._run('[*] 进行同步线路测试 ... ', self.testsynccheck)
        playWeChat = 0
        redEnvelope = 0
        while True:
            self.lastCheckTs = time.time()
            [retcode, selector] = self.synccheck()
            if self.DEBUG:
                print 'retcode: %s, selector: %s' % (retcode, selector)
            logger.debug(
                '====================retcode: %s, selector: %s====================='
                % (retcode, selector))
            if retcode == '1100':
                print '[*] 你在手机上登出了微信，债见'
                logger.debug('[*] 你在手机上登出了微信，债见')
                break
            if retcode == '1101':
                print '[*] 你在其他地方登录了 WEB 版微信，债见'
                logger.debug('[*] 你在其他地方登录了 WEB 版微信，债见')
                break
            elif retcode == '0':
                if selector == '2':
                    r = self.webwxsync()
                    if r is not None: self.handleMsg(r)
                elif selector == '6' or selector == '3':
                    # TODO
                    logger.debug("CY debugging ========= %s =======BEGIN" %
                                 selector)
                    r = self.webwxsync()
                    if r is not None: self.handleMsg(r)
                    logger.debug("CY debugging ==================END")
                    redEnvelope += 1
                    print '[*] 收到疑似红包消息 %d 次' % redEnvelope
                    logger.debug('[*] 收到疑似红包消息 %d 次' % redEnvelope)
                elif selector == '7':
                    playWeChat += 1
                    print '[*] 你在手机上玩微信被我发现了 %d 次' % playWeChat
                    logger.debug('[*] 你在手机上玩微信被我发现了 %d 次' % playWeChat)
                    r = self.webwxsync()
                elif selector == '0':
                    logger.debug("CY is this correct case ? ========")
                    time.sleep(1)
            if (time.time() - self.lastCheckTs) <= 20:
                time.sleep(time.time() - self.lastCheckTs)

    def sendMsg(self, name, word, isfile=False):
        id = self.getUSerID(name)
        if id:
            if isfile:
                with open(word, 'r') as f:
                    for line in f.readlines():
                        line = line.replace('\n', '')
                        self._echo('-> ' + name + ': ' + line)
                        if self.webwxsendmsg(line, id):
                            print ' [成功]'
                        else:
                            print ' [失败]'
                        time.sleep(1)
            else:
                if self.webwxsendmsg(word, id):
                    print '[*] 消息发送成功'
                    logger.debug('[*] 消息发送成功')
                else:
                    print '[*] 消息发送失败'
                    logger.debug('[*] 消息发送失败')
        else:
            print '[*] 此用户不存在'
            logger.debug('[*] 此用户不存在')

    def sendMsgToAll(self, word):
        for contact in self.ContactList:
            logger.debug(contact)
            name = contact['RemarkName'] if contact['RemarkName'] else contact[
                'NickName']
            logger.debug(name)
            id = contact['UserName']
            logger.debug(id)
            self._echo('-> ' + name + ': ' + word)
            #if self.webwxsendmsg(word, id):
            #	print ' [成功]'
            #else:
            #		print ' [失败]'
            #		time.sleep(1)

    def sendImg(self, name, file_name):
        print "CY enter sendImg"
        response = self.webwxuploadmedia(file_name)
        media_id = ""
        if response is not None:
            print "CY media id is =", response['MediaId']
            media_id = response['MediaId']
        #user_id = self.getUSerID(name)
        response = self.webwxsendmsgimg(name, media_id, file_name)

    @catchKeyboardInterrupt
    def start(self):
        self._echo('[*] 微信网页版 ... 开动')
        print
        logger.debug('[*] 微信网页版 ... 开动')
        while True:
            self._run('[*] 正在获取 uuid ... ', self.getUUID)
            self._echo('[*] 正在获取二维码 ... 成功')
            print
            logger.debug('[*] 微信网页版 ... 开动')
            self.genQRCode()
            print '[*] 请使用微信扫描二维码以登录 ... '
            if not self.waitForLogin():
                continue
                print '[*] 请在手机上点击确认以登录 ... '
            if not self.waitForLogin(0):
                continue
            break

        self._run('[*] 正在登录 ... ', self.login)
        self._run('[*] 微信初始化 ... ', self.webwxinit)
        self._run('[*] 开启状态通知 ... ', self.webwxstatusnotify)
        self._run('[*] 获取联系人 ... ', self.webwxgetcontact)
        self._echo('[*] 应有 %s 个联系人，读取到联系人 %d 个' %
                   (self.MemberCount, len(self.MemberList)))
        print
        self._echo('[*] 共有 %d 个群 | %d 个直接联系人 | %d 个特殊账号 ｜ %d 公众号或服务号' %
                   (len(self.GroupList), len(self.ContactList),
                    len(self.SpecialUsersList), len(self.PublicUsersList)))
        print
        self._run('[*] 获取群 ... ', self.webwxbatchgetcontact)
        logger.debug('[*] 微信网页版 ... 开动')
        if self.DEBUG: print self
        logger.debug(self)

        self.autoReplyMode = True

        #if self.interactive and raw_input('[*] 是否开启自动回复模式(y/n): ') == 'y':
        #	self.autoReplyMode = True
        #	print '[*] 自动回复模式 ... 开启'
        #		logger.debug('[*] 自动回复模式 ... 开启')
        #		else:
        #			print '[*] 自动回复模式 ... 关闭'
        #E			logger.debug('[*] 自动回复模式 ... 关闭')

        sid = sys.argv[1]
        print "wxbot.py  WeiXin logging in is DONE......."
        os.system("/bin/echo LOGIN > out/%s/login.txt" %(sid))

        listenProcess = multiprocessing.Process(target=self.listenMsgMode)
        listenProcess.start()

        while True:
            text = raw_input('')
            if text == 'quit':
                listenProcess.terminate()
                print('[*] 退出微信')
                logger.debug('[*] 退出微信')
                exit()
            elif text[:2] == '->':
                [name, word] = text[2:].split(':')
                if name == 'all': self.sendMsgToAll(word)
                else: self.sendMsg(name, word)
            elif text[:3] == 'm->':
                [name, file] = text[3:].split(':')
                self.sendMsg(name, file, True)
            elif text[:3] == 'f->':
                print '发送文件'
                logger.debug('发送文件')
            elif text[:3] == 'i->':
                print '发送图片'
                [name, file_name] = text[3:].split(':')
                self.sendImg(name, file_name)
                logger.debug('发送图片')

    def _safe_open(self, path):
        if self.autoOpen:
            if platform.system() == "Linux":
                os.system("xdg-open %s &" % path)
            else:
                os.system('open %s &' % path)

    def _run(self, str, func, *args):
        self._echo(str)
        if func(*args):
            print '成功'
            logger.debug('%s... 成功' % (str))
        else:
            print('失败\n[*] 退出程序')
            logger.debug('%s... 失败' % (str))
            logging.debug('[*] 退出程序')
            exit()

    def _echo(self, str):
        sys.stdout.write(str)
        sys.stdout.flush()

    def _printQR(self, mat):
        for i in mat:
            BLACK = '\033[40m  \033[0m'
            WHITE = '\033[47m  \033[0m'
            print ''.join([BLACK if j else WHITE for j in i])

    def _str2qr(self, str):
        qr = qrcode.QRCode()
        qr.border = 1
        qr.add_data(str)
        mat = qr.get_matrix()
        self._printQR(mat)  # qr.print_tty() or qr.print_ascii()

    def _transcoding(self, data):
        if not data: return data
        result = None
        if type(data) == unicode:
            result = data
        elif type(data) == str:
            result = data.decode('utf-8')
        return result

    def _get(self, url, api=None):
        url = re.sub(r"@[\d\w]+:<br/>", "", url)
        url = re.sub(r"<br/>", "", url)
        #logger.debug("CY _get url %s"%url)
        request = urllib2.Request(url=url)
        request.add_header('Referer', 'https://wx.qq.com/')
        if api == 'webwxgetvoice': request.add_header('Range', 'bytes=0-')
        if api == 'webwxgetvideo': request.add_header('Range', 'bytes=0-')
        try:
            response = urllib2.urlopen(request)
            data = response.read()
            logger.debug(url)
            return data
        except:
            logger.debug("excption in _get %s" % url)

    def _post(self, url, params, jsonfmt=True):
        if jsonfmt:
            request = urllib2.Request(url=url, data=json.dumps(params))
            request.add_header('ContentType',
                               'application/json; charset=UTF-8')
        else:
            request = urllib2.Request(url=url, data=urllib.urlencode(params))
        try:
            response = urllib2.urlopen(request)
            data = response.read()
            if jsonfmt: return json.loads(data, object_hook=_decode_dict)
            return data
        except:
            logger.debug("excption in _post %s" % url)
            return None

    def _smart(self, word, uid):
        logger.debug(uid)
        uid2 = uid[2:66]
        url = 'http://i2.jiqid.com/robot/'
        text = re.sub(r"@[\d\w]+:<br/>", "", word)
        text = re.sub(r"<br/>", "", text)
        text = text.replace('#', '')
        text = text.replace('＃', '')
        #text = text.replace('@','')
        text = text.replace('@流氓兔', '')

        if len(text) == 0:
            return "what's up?"

        payload = {'text': text, 'uid': uid2, 'type': 0, 'tts': 0}
        #    r = requests.post(url, json = payload)

        resp = ""
        #if r is not None and r.text is not None:
        try:
            r = requests.post(url, json=payload)
            data = json.loads(r.text)
            if 'title' in data:
                resp += data['title']
            if 'body' in data:
                resp += data['body']
            if 'url' in data:
                resp += data['url']
        except:
            resp = "我没听懂哎"

        if text == resp:
            resp = switchWords[random.randint(0, _nrSwitchWords)]

        logger.debug("CY==================")
        logger.debug(resp)
        return resp.encode('utf-8')

    def _detectPorn(self, path):
        image = Image.open(path)
        return detect.detect(image)

    def _get_token(self):
        #FIXME add cache
        apiKey = "DrLHArA9fNxO0ueRGTj0M7oP"
        secretKey = "c5795c38aba4463fa59002e5b553962b"
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        return json.loads(json_data)['access_token']

    def _audio2Text(self, path):
        file_amr = path.replace("mp3", "amr")
        cmd = "./bin/ffmpeg -i " + path + " -ar 8000 -ac 1 " + file_amr
        logger.debug(cmd)
        rc = os.system(cmd)  #FIXME check the rc

        token = self._get_token()
        logger.debug(token)

        f = open(file_amr, 'r')
        if f is not None:
            speech = base64.b64encode(f.read())
            size = os.path.getsize(file_amr)
            update = json.dumps({
                'format': 'amr',
                'rate': '8000',
                'channel': 1,
                'cuid': "baider",
                'token': token,
                'speech': speech,
                'len': size
            })
            r = urllib2.urlopen('http://vop.baidu.com/server_api', update)

            t = r.read()
            result = json.loads(t)
            logger.debug(result)
            if result['err_msg'] == 'success.':
                word = result['result'][0].encode('utf-8')
                if word != '':
                    if word[len(word) - 3:len(word)] == '，':
                        return word[0:len(word) - 3]
                    else:
                        return word
                else:
                    return ''
            else:
                return ""

        return ''

    def _searchContent(self, key, content, fmat='attr'):
        if fmat == 'attr':
            pm = re.search(key + '\s?=\s?"([^"<]+)"', content)
            if pm: return pm.group(1)
        elif fmat == 'xml':
            pm = re.search('<{0}>([^<]+)</{0}>'.format(key), content)
            if not pm:
                pm = re.search('<{0}><\!\[CDATA\[(.*?)\]\]></{0}>'.format(key),
                               content)
            if pm: return pm.group(1)
        return '未知'


class UnicodeStreamFilter:
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding

    def write(self, s):
        if type(s) == str:
            s = s.decode('utf-8')
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

    def flush(self):
        self.target.flush()


if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)

if __name__ == '__main__':
    sid = sys.argv[1]
    os.system("rm out/%s/login.txt" %(sid))

    newPath1 = "/var/www/html/%s-1.jpg"%sid;
    newPath2 = "/var/www/html/%s-2.jpg"%sid;
    if os.path.exists(newPath1):
        os.remove(newPath1)
    if os.path.exists(newPath2):
        os.remove(newPath2)


    wspace = "out/%s"%sid
    logPath = "%s/log.txt"%(wspace)
    pidPath = "%s/pid.txt"%(wspace)
    savedPath = "%s/saved"%(wspace)
    if not os.path.exists(savedPath):
        os.makedirs(savedPath)

    if not os.path.exists(savedPath+"/msgimgs"):
        os.makedirs(savedPath+"/msgimgs")

    if not os.path.exists(savedPath+"/videos"):
        os.makedirs(savedPath+"/videos")

    if not os.path.exists(savedPath+"/voices"):
        os.makedirs(savedPath+"/voices")

    pid = os.getpid()
    os.system("/bin/echo %s > %s" %(pid, pidPath))
    load_gif_repo()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logPath)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    #import coloredlogs
    #coloredlogs.install(level='ERROR')

    webwx = WebWeixin()
    webwx.start()
