#!/usr/bin/env python
import datetime
import threading
import sys
from time import ctime, sleep

def music(req):
    print 'music thread(param:%s)...' %(req)
    sleep(1)

def movie(req):
    print 'movie thread(param:%s)...' %(req)
    sleep(2)
## main entry
print '===main started process'
threads = []

cur = datetime.datetime.now()
print '%s > start t1...' %(cur.strftime('%H:%M:%S'))
t1 = threading.Thread(target=music, args = ('hello',))
t1.setDaemon(True)
t1.start()
print '    < start t1...'
cur = datetime.datetime.now()
print '%s > start t2...' %(cur.strftime('%H:%M:%S'))
t2 = threading.Thread(target=movie, args = ('world',))
t2.setDaemon(True)
t2.start()
print '    < start t2...'

t1.join()
t2.join()

print '===main thread exited'

