# coding: utf-8

import os
import sys
import time
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=1)

def killBot(sid):
    print "killBot"
    try:
        os.system("ps -ef | grep 'wxmain.py %s' | grep -v grep | awk '{print $2}' | xargs kill -9"%(sid))
    except:
            print "error in kill , probably none of this process"

    return 0

def isExisting(sid):
    if not os.path.exists("./out/%s"%sid):
    #    print "Never starte..Not existed"
        return False

    os.system("ps -ef | grep 'wxmain.py %s' | grep -v grep | awk '{print $2}' > ./out/%s/existed.txt"%(sid,sid))

    with open("./out/%s/existed.txt"%sid) as f:
        pid = f.readline()
        if pid == "":
     #       print "Not existed"
            return False
        else:
      #      print "Existed"
            #FIXME : compare the realtime pid with that in pid.txt
            return True


def isLogin(sid):
    status = mc.get("WX:%s:status"%sid)
    #print "isLogin %s"%status
    if status:
        if status == "success":
            return True

    return False

def startBot(sid):
    print "enter Start Bot"
    if isExisting(sid):
        print "====Bot %s is there=============="%sid
        return 1
    else:
        print "=============startBot============="
        os.system("python ../wx2/wxmain.py %s &"%sid)
        return 0

def stopBot(sid):
    print "==============stopBot================"
    if isExisting(sid):
        print "try kill..."
        try:
            os.system("ps -ef | grep 'wxmain.py %s' | grep -v grep | awk '{print $2}' | xargs kill -9"%(sid))
            print ("ps -ef | grep 'wxmain.py %s' | grep -v grep | awk '{print $2}' | xargs kill -9"%(sid))
        except:
            print "error in kill , probably none of this process"
        
        mc.delete("WX:%s:status"%sid)
        return 0
    else:
        print "bot was not started"
        #clear the flag just in case
        mc.delete("WX:%s:status"%sid)
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
        print "===do Restart Bot===="
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
    #print "exit with %d"%rc
    exit(rc)

