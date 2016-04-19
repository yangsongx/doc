#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import time
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

import random

white_list = ""
switchWords = ["换个话题吧","我们聊聊其他的吧","说说最新的新闻怎么样","有什么好玩的事情"]
_nrSwitchWords =len(switchWords) -1

class MyWXBot(WXBot):

    def __init__(self, bot_id):
        WXBot.__init__(self, bot_id)
        self.robot_switch = True

    def _smart(self, word, uid):
        if True:
            url = 'http://i2.jiqid.com/robot/'
            uid = uid[2:66]
            payload = {'text': word, 'uid':uid ,'type': 0, 'tts': 0}

            resp = ""
            try:
                logger.debug( time.time())
                r = requests.post(url, json =payload)
                data = json.loads(r.text)
                if 'title' in data:
                    resp += data['title']
                if 'body' in data:
                    resp += data['body']
                if 'url' in data:
                    resp += data['url']
            except:
                resp = "我没听懂哎"
              
            logger.debug( time.time())
            return resp.encode('utf-8')


    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        logger.debug(msg)
        try:
            if not self.robot_switch and msg['msg_type_id'] != 1:
                logger.debug("run in switch")
                return
            if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
                logger.debug("reply to self")
                self.auto_switch(msg)
            elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
                logger.debug("reply to somebody")
                self.send_msg_by_uid(self._smart(msg['content']['data'], msg['user']['id']), msg['user']['id'])
            elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
                logger.debug("reply to group")
                if 'detail' in msg['content']:
                    logger.debug("CY -1")
                    my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                    if my_names is None:
                        my_names = {}
                    if 'NickName' in self.my_account and self.my_account['NickName']:
                        my_names['nickname2'] = self.my_account['NickName']
                    if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                        my_names['remark_name2'] = self.my_account['RemarkName']
                        
                    logger.debug("CY -2")

                    is_at_me = False
                    for detail in msg['content']['detail']:
                        if detail['type'] == 'at':
                            for k in my_names:
                                if my_names[k] and my_names[k] == detail['value']:
                                    is_at_me = True
                                    break
                    if is_at_me:
                        logger.debug("CY -3")

                        src_name = msg['content']['user']['name']
                        #reply = 'to ' + src_name + ': '
                        reply = ""
                        if msg['content']['type'] == 0:  # text message
                            reply += self._smart(msg['content']['desc'], msg['content']['user']['id'])
                        else:
                            reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,???,,"
                        self.send_msg_by_uid(reply, msg['user']['id'])
        except:
            import sys
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            logger.debug('an exception' + info)

'''
    def schedule(self):
    self.send_msg('tb', 'schedule')
    time.sleep(1)
'''


def main():
    bot = MyWXBot(sys.argv[1])
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    os.system("mkdir -p out/%s/"%sys.argv[1])
    logPath = "out/%s/log.txt"%(sys.argv[1])
    logger = logging.getLogger("wxbot")
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

    # load whileList
    fn = 'out/%s/whitelist'%sys.argv[1]
    try:
        with open(fn, 'r') as f:
            white_list = f.read();
            white_list = white_list.split('/')
            #print "list=: ", white_list
    except:
        logger.debug("whitelist file is not there")
        

    main()
