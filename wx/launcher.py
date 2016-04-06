# coding: utf-8

import os
import sys
import time

def killBot(path):
    with open(path) as f:
        pid = int(f.readline())
        print "start killing proces"
        os.kill(pid, 9)

def startBot(sid):
    os.system("python ./wxbot.py %s >/dev/null 2>/dev/null &"%sid)

if __name__ == "__main__":
    sid = sys.argv[1]
    startBot(sid)

    time.sleep(5)

    pidPath = "./out/%s/pid.txt"%sid
    print pidPath
    killBot(pidPath)
