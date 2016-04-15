#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import time
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

import random


switchWords = ["换个话题吧","我们聊聊其他的吧","说说最新的新闻怎么样","有什么好玩的事情"]
_nrSwitchWords =len(switchWords) -1

class MyWXBot(WXBot):
    def _smart(self, word):
        if True:
            url = 'http://i2.jiqid.com/robot/'

            payload = {'text': word, 'uid':"tester" ,'type': 0, 'tts': 0}

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

    def handle_msg_all(self, msg):
        logger.debug( "CY",msg)
        #return
        try:	
            if ( msg['msg_type_id'] == 4  or msg['msg_type_id'] ==3 ) and msg['content']['type'] == 0 and ('ChenYang' in msg['user']['name'] or '流氓兔' in msg['user']['name'] or 'ChenYang' in msg['content']['user']['name'] or '流氓兔' in msg['content']['user']['name']):
                logger.debug( "do smart")
                time.sleep(2)
                resp = self._smart(msg['content']['data'])
                print( msg['content']['data'], resp)
                if resp == msg['content']['data']:
                    logger.debug( "repeated")
                    resp = switchWords[random.randint(0, _nrSwitchWords)]
                else:
                    logger.debug( "not same")

                if len(resp) > 150:
                    tmp = resp.decode('utf-8')
                    resp = tmp[:40].encode('utf-8')
                logger.debug(type(resp))
                logger.debug(resp)

                self.send_msg_by_uid(resp, msg['user']['id'])
            else:
                logger.debug( "skip")
        except:
            logger.debug( "err01")
          

'''
    def schedule(self):
    self.send_msg('tb', 'schedule')
    time.sleep(1)
'''


def main():
    bot = MyWXBot(sys.argv[1])
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
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

    main()
