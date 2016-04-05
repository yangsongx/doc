#coding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from GeneratePackage import do_generate_packages
from models import Packages
from models import PbType
from models import PbInfo
from models import Rawfiles
import logging
import json

logger = logging.getLogger("django")


def do_upload_json(mid, js_data):
    #step 1: clear db records with maker_id in rawfiles and packages
    ret = {}
    if mid < 0:
        ret['code'] = '40'
        print 'invalid maker id:%s' % mid
        return ret
    try:
        obj = Rawfiles.objects.filter(pac=int(mid))
        if len(obj) <= 0:
            print 'no history recored with maker_id:%s' % mid
        else:
            print "will clear the records in rawfils with maker_id:%s" % mid
            obj.delete()
        for r in js_data['data']:
            print r
            #
            #   pac_id: maker id            
            #    pb_type_ID: resource type id ,for not prebuilt resourse, this is needed
            #    pb_info_ID: prebuilt info id
            #    name: uploaded file name
            #    download_url: download buket key on qiniu, for prebuilt resourse, set null
            #    suffix: unused
            #    modified: null
            #    crop: crop info for audio and imgs
            #    processed_url: processed url such as ringer
            obj = Rawfiles(\
                           pac_id=int(mid),\
                           pb_type=PbType(id=int(r[0])),\
                           pb_info=PbInfo(id=int(r[1])),\
                           name=r[2],\
                           download_url=r[3],\
                           suffix=r[4],\
                           modified=r[5], \
                           crop=r[6],\
                           processed_url=r[7]\
                          )
            obj.save()
        #ret['code'] = '0'
        ret = do_generate_packages(mid)
    except Exception, e:
        print ">>>>>>>>>>>>>>>>>>>>>>>>???????????????"
        print e
        ret['code'] = '70'  #incorrect request
    return ret


#####################################################################################
# @type_txt : The textual description, such as boot-1, wallpaper
#
# return the mapping ID in DB pb_type, or -1 for non-existence txt
#
def map_type_id(type_txt):

    map_table = {
        'callringtone': 1,
        'uptone': 2,
        'lock': 3,
        'wallpaper': 4,
        'smstone': 5,  #FIXME - currently web not support yet
        'app': 6,
        'welcome': 7,  #'boot-1' : 1001,
        #        'boot-2' : 1002,
        #        'boot-3' : 1003,
        #        'boot-4' : 1004
    }

    if type_txt.startswith('boot-'):
        tmp = type_txt[5:len(type_txt)]
        i = int(tmp)
        i += 1000  # Note, boot- start with 1000 offset
    else:
        i = map_table.get(type_txt)
        if i is None:
            logger.warning('Well, invalide type text, set it as -1')
            i = -1

    return i
