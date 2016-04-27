# coding: utf-8

from wxbot import *
import time
import logging

import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import random

white_list = ""
switchWords = ["换个话题吧","我们聊聊其他的吧","说说最新的新闻怎么样","有什么好玩的事情"]
_nrSwitchWords =len(switchWords) -1

key2Gif = {
    'hello': {"in": ["你好", "在吗"],
           "out": ["你好"]},
    'who': {"in": ["你是谁"],
            "out": ["我是"]},
    'girl': {"in": ["美女"],
            "out": ["美女"]},

    'boy': {"in": ["帅哥"],
            "out": ["帅哥"]},

    'bishi': {"in": ["鄙视", "阴险"],
            "out": ["鄙视", "阴险"]},
    'bye': {"in": ["再见", "拜拜"],
           "out": ["再见", "拜拜"]},
    'naive': {"in": ["你好可爱"],
           "out": ["人见人爱"]},
    'photo': {"in": ["发照片", "你的照片", "发张照片","美女","帅哥","美"],
            "out": []},
    'money': {"in": ["红包"],
              "out": ["红包"]},
    'pity': {"in": [],
           "out": []},
    'cry': {"in": ["哭", "呜呜"],
          "out": ["哭", "呜呜"]},
    'morning': {"in": ["早上好", "早啊"],
            "out": ["早上好", "早啊"]},
    'night': {"in": ["晚安"],
           "out": ["晚安"]},
    'laugh': {"in": ["哈哈", "呵呵", "笑脸"],
          "out": ["哈哈", "哈皮"]},
    'thanks': {"in": ["谢谢", "感谢"],
           "out": ["不客气", "谢谢"]},
    'admir': {"in": ["牛逼", "赞", "厉害"],
          "out": ["赞"]},
}

gifDic = {}


def load_gif_repo():
    rootdir = "./gif/"
    if os.path.exists("/d/gif/"):
        rootdir = "/d/gif/"
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
    cate = "others"
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
    if cate == 'photo':
        ratio = 1
    return getGifByCate(cate), ratio, cate

class MyWXBot(WXBot):

    def __init__(self, bot_id):
        WXBot.__init__(self, bot_id)
        self.robot_switch = True


    def _respond_gif(self, word, resp, to, po):
        gifFile, ratio, cate = pick_gif_per_text(word, resp)
        logger.debug(gifFile)
        ifShow = 1
        if ratio < 1:
            a = random.randint(0, po)
            if a > (po-2):
                ifShow = 1
            else:
                ifShow = 0

        if ifShow == 1:
        #if True:
            if gifFile is not None:
                self.send_image(to, gifFile)


    def _smart(self, word, uid):
        if True:
            url = 'http://i2.jiqid.com/robot/'
            uid2 = uid[2:66]
            payload = {'text': word, 'uid':uid2 ,'type': 0, 'tts': 0}

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

            resp = resp.replace("米小兔", "流氓兔")
            resp = resp.replace("米兔", "流氓兔")
            resp = resp.replace("图灵机器人", "")
            resp = resp.replace("机器岛", "世界")
            resp = resp.replace("你说的内容我暂时还没法理解", "哦")
             
            '''
            gifFile, ratio, cate = pick_gif_per_text(word, resp)
            logger.debug(gifFile)
            ifShow = 1
            if ratio < 1:
                ifShow = random.randint(0, 5)

            #if ifShow > 3:
            if True:
                if gifFile is not None:
                    logger.debug(gifFile)
                    self.send_image(uid, gifFile)
            '''
            self._respond_gif(word, resp, uid, 4)
 
            logger.debug( time.time())
            print 'answer:%s ===> %s' %(word, resp.encode('utf-8'))
            # FIXME - the @uid here maybe need parse section instead of whole data inserted into DB....
            self.record_into_db(uid, word, resp.encode('utf-8'))
            return resp.encode('utf-8')


# FIXME - need a reasonable method for writing to DB
# * pre-connect to DB will be resource-wasting if too much process running
# * one-connect on one-write will be performance-latency
    def record_into_db(self, uid, ques, ans):
        try:
            db = MySQLdb.connect(user='root',
                db = 'maker',
                passwd='robotlite@8',
                host='www.ioniconline.com',
                port=33060)
            print 'connected [OK]'
            cursor = db.cursor()
            sql_cmd = 'INSERT INTO uc_usermessagedata (q,a,user_id) VALUES (\'%s\', \'%s\', \'%s\')' \
                    %(ques, ans, uid)
            cursor.execute(sql_cmd)
            db.commit()
            db.close()
            print 'write into DB [OK]'
        except:
            info = "+%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            print info

        return 0

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
                resp = self._smart(msg['content']['data'], msg['user']['id'])
                self.send_msg_by_uid(resp, msg['user']['id'])
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
                    if not is_at_me:
                        if "#" in msg['content']['desc'] or "@" in msg['content']['desc'] or "流氓兔" in msg['content']['desc']:
                            is_at_me = True
                    if is_at_me:
                        logger.debug("CY -3")

                        src_name = msg['content']['user']['name']
                        #reply = 'to ' + src_name + ': '
                        reply = ""
                        if msg['content']['type'] == 0:  # text message
                            reply += self._smart(msg['content']['desc'], msg['user']['id'])
                        else:
                            reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,???,,"
                        self.send_msg_by_uid(reply, msg['user']['id'])
                    else:
                        word = msg['content']['desc']
                        self._respond_gif(word, word, msg['user']['id'], 10)
            elif msg['msg_type_id'] == 3 and msg['content']['type'] == 4:  # group voice message
                file_path = msg['content']['path']
                asr = self._audio2Text(file_path)
                src_name = msg['content']['user']['name']
                logger.debug(src_name)
                if asr != "":
                    resp = "[微信助手] %s说: %s" % (src_name, asr)
                else:
                    resp = "[微信助手] 无法识别%s刚刚的语音消息，暂时只支持普通话" % src_name
                self.send_msg_by_uid(resp, msg['user']['id'])

                if True:
                    try:
                        #if "兔" in asr:
                        if True:
                            resp = self._smart(asr, msg['user']['id'])
                            self.send_msg_by_uid(resp, msg['user']['id'])
                    except:
                        logger.debug("failed to send resp")

            elif msg['msg_type_id'] == 4 and msg['content']['type'] == 4:  # private voice message
                file_path = msg['content']['path']
                asr = self._audio2Text(file_path)
                src_name = msg['user']['name']
                logger.debug(src_name)
                if asr != "":
                    resp = "[微信助手] %s说: %s" % (src_name, asr)
                else:
                    resp = "[微信助手] 无法识别%s刚刚的语音消息，暂时只支持普通话" % src_name
                self.send_msg_by_uid(resp, msg['user']['id'])

                if True:
                    try:
                        resp = self._smart(asr, msg['user']['id'])
                        self.send_msg_by_uid(resp, msg['user']['id'])
                    except:
                        logger.debug("failed to send resp")

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
    load_gif_repo()
    bot = MyWXBot(sys.argv[1])
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    #bot.conf['qr'] = 'tty'
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
