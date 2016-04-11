# coding: utf-8

import memcache
import sys

mc = memcache.Client(['127.0.0.1:11211'], debug=1)
print mc.get("WX:%s:status"%sys.argv[1])
