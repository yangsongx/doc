#coding:utf-8
import datetime
from qiniu import Auth
import string
from task import createZipBall
from webviews.models import Packages
import sys
import os
import random
import utils


# this will generate a random pin code to indicate a customized package
def __my_createpincode():
    num = random.randint(0, 9999)
    # Note - char don't use O,I and l
    s = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q', \
                                   'p','n','m','k','j','h','g', \
                                   'f','e','d','c','b','a'],2)) \
            .replace(' ','')
    ret = '%s%04d' % (s, num)
    # need scratch above data again
    ret2 = list(ret)
    random.shuffle(ret2)
    ret3 = ''.join(ret2)
    return ret3

#####################################################################################
# 2015-09-10 As very tough schedule, use a simpler random pin code,
#            which is just 6-digit.
def __my_createpincode_numerical():
    num = random.randint(100000, 999999)
    code = '%06d' % (num)
    return code

def __my_qiniutoken():
    access_key = '5haoQZguw4iGPnjUuJnhOGufZMjrQnuSdySzGboj'
    secret_key = 'OADMEtVegAXAhCJBhRSXXeEd_YRYzEPyHwzJDs95'
    q = Auth(access_key, secret_key)
    return q.upload_token('cdstatic')


def do_generate_packages(mid):
    try:
        print 'DEBUG going to the background maker...'
        ret = {}
        ret['code'] = '50'
        if mid != -1:
            # TODO - will use my_qiniutoken() to pass a token to consumer
            tok = __my_qiniutoken()
            handler = createZipBall.delay(tok, mid)
            print 'DEBUG waiting...'
            handler.wait()
            # Note - consumer download,package, and upload, give a MD5
            # after wait(), here will try generate a uuid-like pincode
            # to mark the package

            st, fsize, md5 = handler.get()
            print '-the MQ handling result is: %s|%s ' % (st, md5)

            if st == 200:
                # try update the package data

                obj = Packages.objects.get(id=mid)

                # 2015-09-10 Use random 6-digit code
                #code = __my_createpincode()
                code = __my_createpincode_numerical()

                # for the new package, pincode need be a new created one
                if obj.md5 is None:
                    obj.pincode = code
                    ret['pinCode'] = code
                else:
                    if obj.pincode is None:
                        obj.pincode = code
                        ret['pinCode'] = code
                    else:
                        ret['pinCode'] = obj.pincode

                obj.md5 = md5
                dt = datetime.datetime.now()
                obj.completed = dt.strftime('%Y-%m-%d %H:%M:%S')
                obj.size = fsize
                obj.save()

                ret['code'] = '0'

            else:
                print 'seems sth wrong(http status:%s)' % (st)
                ret['code'] = st
        else:
            ret['code'] = '51'  #incorrect request
    except:
        base_dir = utils.get_base_dir()
        os.chdir(base_dir)
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        print 'an exception' + info
        ret['code'] = '52'  #incorrect request
    return ret
