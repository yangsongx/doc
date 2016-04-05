# coding: utf-8


import requests
import json
import sys

url = 'http://i2.jiqid.com/robot/'
payload = {'text': sys.argv[1], 'uid':'Weixin','type': 0, 'tts': 0}

r = requests.post(url, json = payload)
data = json.loads(r.text)
print data['title']


   
def _smart(word):
        url = 'http://i2.jiqid.com/robot/'
        payload = {'text': word, 'uid':'Weixin','type': 0, 'tts': 0}
        r = requests.post(url, json = payload)
        data = json.loads(r.text)
        resp = ""
        if 'title' in data: 
            resp += data['title']
        if 'body' in data: 
            resp += data['body']
        if 'url' in data: 
            resp += data['url']
        return resp


print  _smart(sys.argv[1])

aa = "@832b05dcd10ec39f819e67ad87dd479898f8beafc9e4513fae1ddaaf7bfaaeee:<br/>呆呆熊是什么<br/>"
aa = re.sub(r"@[\d\w]+:<br/>","", aa)
print aa
