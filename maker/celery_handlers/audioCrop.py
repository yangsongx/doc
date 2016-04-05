#coding:utf-8
import os
from qiniu import put_file, Auth
import utils

from django.db import models
from django.utils.translation import ugettext_lazy as _
from models import Packages
from models import Rawfiles
import urllib2


#must install ffmpeg(apt-get install ffmpeg)
def upload_cropped_file(file_path, mid, md5_orig, crop_orig):
    access_key = '5haoQZguw4iGPnjUuJnhOGufZMjrQnuSdySzGboj'
    secret_key = 'OADMEtVegAXAhCJBhRSXXeEd_YRYzEPyHwzJDs95'
    q = Auth(access_key, secret_key)
    up_token = q.upload_token('cdstatic')
    key = utils.get_md5(file_path)

    ret, info = put_file(up_token, key, file_path)
    if info.status_code != 200:
        return -4
    #update database
    obj = Rawfiles.objects.filter(pac=mid,
                                  download_url=md5_orig,
                                  crop=crop_orig)
    if len(obj) <= 0:
        print 'no history recored with maker_id:%s' % mid
        return -5
    print "audio crop: update record %s,%s" % (mid, md5_orig)
    obj.update(processed_url=key)
    return 0


def audio_crop(input_file, output_file, ss, duration, mid, md5_orig, crop_orig
               ):
    input_file = urllib2.unquote(input_file)
    output_file = urllib2.unquote(output_file)
    if os.path.exists(output_file):
        os.remove(output_file)
    cmd = "ffmpeg -ss " + str(ss) + " -t " + str(
        duration) + " -i " + input_file + " " + output_file
    print "audo crop cmd=%s" % cmd
    ret = os.system(cmd)
    if not os.path.exists(output_file):
        print "can't create crop file for %s, %s" % (input_file, output_file)
        return -3
    if os.path.getsize(output_file) < 1024:
        print "output file too small"
        return -1
    if ret == 0:
        return upload_cropped_file(output_file, mid, md5_orig, crop_orig)
    return -2
