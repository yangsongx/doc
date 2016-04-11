#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import time
import sys

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
                time.sleep(3)
                resp = self._smart(msg['content']['data'])
                logger.debug( msg['content']['data'], resp)
                if resp == msg['content']['data']:
                    logger.debug( "repeated")
                    resp = switchWords[random.randint(0, _nrSwitchWords)]
                else:
                    logger.debug( "not same")

                self.send_msg_by_uid(resp[:20], msg['user']['id'])
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
    import logging
    os.system("mkdir -p out/%s/"%sys.argv[1])
    logPath = "out/%s/log.txt"%(sys.argv[1])

    # 配置日志信息  
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',  
                    datefmt='%m-%d %H:%M',  
                    filename=logPath,  
                    filemode='w')  

    logger = logging.getLogger("wxmain")

    bot = MyWXBot(sys.argv[1])
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
