# coding: utf-8

import os
import sys
import time

def killBot(path):
    print "killBot"
    sid = sys.argv[2]
    with open(path) as f:
        pid = int(f.readline())
        print "start killing proces"
        print "ps -ef | grep 'wxbot.py %s' | grep -v grep | awk '{print $2}' | xargs kill -9"%(sid)
        try:
            #os.kill(pid, 9)
            os.system("ps -ef | grep 'wxbot.py %s' | grep -v grep | awk '{print $2}' | xargs kill -9"%(sid))
        except:
            print "error in kill , probably none of this process"

    return 0

def isExisting(sid):
    if not os.path.exists("./out/%s"%sid):
        print "Never starte..Not existed"
        return False

    os.system("ps -ef | grep 'wxbot.py %s' | grep -v grep | awk '{print $2}' > ./out/%s/existed.txt"%(sid,sid))
    print ("ps -ef | grep %s | grep -v grep | awk '{print $2}' > ./out/%s/existed.txt"%(sid,sid))
    with open("./out/%s/existed.txt"%sid) as f:
        pid = f.readline()
        if pid == "":
            print "Not existed"
            return False
        else:
            print "Existed"
            #FIXME : compare the realtime pid with that in pid.txt
            return True


def isLogin(sid):
    if not os.path.exists("./out/%s/login.txt"%sid):
        print "not started in islogin"
        return False

    with open("./out/%s/login.txt"%sid) as f:
        pid = f.readline()
        if pid == "":
            print "Not login"
            return False
        else:
            print "login"
            #FIXME : compare the realtime pid with that in pid.txt
            return True


def startBot(sid):
    if isExisting(sid):
        print "====Bot %s is there=============="%sid
        return 1
    else:
        print "=============startBot============="
        os.system("python ../wx/wxbot.py %s &"%sid)
        return 0

def stopBot(sid):
    if isExisting(sid):
        pidPath = "./out/%s/pid.txt"%sid
        print pidPath
        killBot(pidPath)
        if os.path.exists("./out/%s/login.txt"%sid):
            os.remove("./out/%s/login.txt"%sid)
        if os.path.exists("./out/%s/qrcode.jpg"%sid):
            os.remove("./out/%s/qrcode.jpg"%sid)

        return 0
    else:
        print "bot was started"
        return 1

def getStatus(sid):
    '''
       0 -- stop
       1 -- wait
       2 -- login
    '''
    ret = 0
    if isExisting(sid):
        if isLogin(sid):
            ret =2
        else:
            ret =1
    else:
        ret = 0     
    return ret

def main():
    cmd = sys.argv[1]
    sid = sys.argv[2]

    if cmd == "start":
        return startBot(sid)
    elif cmd  == "stop":
        return stopBot(sid)
    elif cmd == "restart":
        stopBot(sid)
        return startBot(sid)
    elif cmd  == "status":
        ret = getStatus(sid)
        return ret
    else:
        print "not supported yet"
        return 1


if __name__ == "__main__":
    rc =main()
    print "exit with %d"%rc
    exit(rc)

