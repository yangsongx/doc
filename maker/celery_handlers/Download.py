#coding:utf-8
import os
import os.path
import urllib2
import time
import md5
from shutil import copy, move, rmtree
from celery import Celery
from celery import shared_task
from celery.result import ResultBase
import Global
import string
from django.db import models
from audioCrop import audio_crop
#from webviews.models import Packages
#from webviews.models import Rawfils
from models import Packages
from models import Rawfiles
from models import PbType
from models import PbInfo
from models import Model

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Downloader:
    def __init__(self, maker_id, url_prefix):
        self.makerid = maker_id
        self.urlPrefix = url_prefix

    def getBootanimList(self):
        r = Rawfiles.objects.filter(pac=int(self.makerid))
        #pb_type=PbType(id>Global.MAKER_BOOTANIMATION_INDEX_START)\
        #)#.order_by(pb_type.id)
        print "Boot animation list len: %d" % len(r)
        #print r[0].pb_type.id
        print r
        return r

    def get_md5(self, full_filename):
        print "full_filename:%s" % full_filename
        unquote_full_filename = urllib2.unquote(full_filename)
        f = file(unquote_full_filename, 'rb')
        return md5.new(f.read()).hexdigest()

    def check_md5(self, correct_md5, full_filename):
        my_md5 = get_md5(full_filename)
        if (my_md5.upper() == correct_md5.upper()):
            return True
        else:
            return False

    def downloadAllfiles(self, resType, model):
        ret_val = Global.MAKER_DOWNLOADER_STATUS_2NOTHING
        result_list = []
        download_path = None
        if resType == Global.RESOURCE_TYPE_ANIMATION:
            os.mkdir(Global.BOOTANIMATION_TMP)
            os.mkdir("bootanimation")
            querySet = self.getBootanimList()
            files_total = len(querySet)
            print ' DEBUG->bootanimation totally %d image...' % (files_total)
            if files_total <= 0:
                print "No bootanimation files found"
                return Global.MAKER_DOWNLOADER_STATUS_2NOTHING, None
            for i in querySet:
                if i.pb_type.id < Global.MAKER_BOOTANIMATION_INDEX_START or i.pb_type.id > Global.MAKER_BOOTANIMATION_INDEX_END:
                    print "pass ####################", i.pb_type.id
                    continue
                print "####################", i.pb_type.id
                if i.download_url != None:
                    file_url = self.urlPrefix + i.download_url
                    filename = (urllib2.quote(str(i.name))).replace('/', '')
                else:
                    #info_obj = PbInfo.objects.get(i.pb_info.id)
                    info_obj = i.pb_info
                    file_url = info_obj.res_file_path
                    filename = (urllib2.quote(str(info_obj.res_name))).replace(
                        '/', '')

                download_path = './' + Global.BOOTANIMATION_TMP
                # handling crop info
                if i.crop is None:
                    print 'contained no-crop info'
                else:
                    print 'non-type case'
                    #crop_size = i.crop.split(':')
                    #imgproc = '?imageMogr2/crop/!%sx%sa%sa%s' %(crop_size[2], crop_size[3], crop_size[0], crop_size[1])
                    #imgproc = '?imageMogr2/crop/!%s' % (i.crop)
                    if (model == "M3"):
                            imgproc = '?imageMogr2/crop/!%s|imageMogr2/thumbnail/720x1280!' % (i.crop)
                    elif (model == "M2D" or model == "M2C"):
                            imgproc = '?imageMogr2/crop/!%s|imageMogr2/thumbnail/480x800!' % (i.crop)
                    else:
                        imgproc = '?imageMogr2/crop/!%s' % (i.crop)
                        print "Not supported model", Global.RESOURCE_TYPE_ANIMATION

                    print 'the extra url:' + imgproc
                    file_url += imgproc
                # handling the format
                suffix = os.path.splitext(filename)[1]
                if suffix != '.png':
                    print 'need %s --> PNG' % (suffix)
                    fmtproc = '/format/png'
                    file_url += fmtproc
                ret_val = self.downloadOneFile(file_url, i.pb_type.id,
                                               download_path)
                if ret_val > 0:
                    print "downloaded file:%s" % file_url
                else:
                    print "downloaded file:%s failed, pls check" % file_url
                    return ret_val, None

            # Next, will try compose the whole directory
            if download_path != None:
                ret_val = self.composeBootImgData(querySet, download_path, model)
            return ret_val, None
        elif resType == Global.RESOURCE_TYPE_PAPER:
            querySet = Rawfiles.objects.filter(pac=int(self.makerid))
            print "len of lock screen:%d" % len(querySet)
            for i in querySet:
                if i.pb_type.id not in [Global.MAKER_PAPER_LOCKSCREEN,
                                        Global.MAKER_PAPER_DESKTOP,
                                        Global.MAKER_PAPER_ECARD]:
                    print "in lock screen, pass type:%d" % i.pb_type.id
                    continue
                if i.download_url == None:
                    file_url = i.pb_info.res_file_path
                else:
                    file_url = self.urlPrefix + i.download_url
                if i.crop:
                    if i.pb_type.id == Global.MAKER_PAPER_DESKTOP:
                        if (model == "M3"):
                                imgproc = '?imageMogr2/crop/!%s|imageMogr2/thumbnail/720x804!' % (i.crop)
                        elif (model == "M2D" or model == "M2C"):
                                imgproc = '?imageMogr2/crop/!%s|imageMogr2/thumbnail/480x498!' % (i.crop)
                        else:
                            print "Not supported model", Global.MAKER_PAPER_DESKTOP
                    elif i.pb_type.id == Global.MAKER_PAPER_LOCKSCREEN:
                        if (model == "M3"):
                                imgproc = '?imageMogr2/crop/!%s|imageMogr2/thumbnail/720x1280!' % (i.crop)
                        elif (model == "M2D" or model == "M2C"):
                                imgproc = '?imageMogr2/crop/!%s|imageMogr2/thumbnail/480x800!' % (i.crop)
                        else:
                            print "Not supported model", Global.MAKER_PAPER_DESKTOP

                    else:
                        imgproc = '?imageMogr2/crop/!%s' % (i.crop)
                    file_url += imgproc

                download_path = './'
                output_file = "paper_type_" + str(i.pb_type.id) + ".png"
                print "IMG files: %s" % i.name
                print "type : %s" % i.pb_type.id
                print "IMG file_url:%s" % file_url
                ret_val = self.downloadOneFile(file_url, i.pb_type.id,
                                               download_path, output_file)
                if ret_val > 0:
                    r = {}
                    r['fileName'] = str(output_file)
                    r['source'] = '1'
                    r['fileMd5'] = self.get_md5(str(output_file))
                    if i.pb_type.id == Global.MAKER_PAPER_LOCKSCREEN:
                        r['paperType'] = "lock"
                    if i.pb_type.id == Global.MAKER_PAPER_DESKTOP:
                        r['paperType'] = "desktop"
                    if i.pb_type.id == Global.MAKER_PAPER_ECARD:
                        r['paperType'] = "ecard"
                    r['paperCode'] = ''
                    r['paperName'] = 'hey paper %d' % i.pb_type.id
                    result_list.append(r)
                else:
                    return ret_val, None

        elif resType == Global.RESOURCE_TYPE_RINGER:
            print 'Now, try download ringer audio file..'
            querySet = self.getAudioFilesList()
            print "len of audio items:%d" % len(querySet)
            for i in querySet:
                if i.pb_type.id not in [Global.MAKER_AUDIO_RINGETONE,
                                        Global.MAKER_AUDIO_UPTONE,
                                        Global.MAKER_AUDIO_MESSAGETONE]:
                    print "pass type for audio: %d" % i.pb_type.id
                    continue
                if i.download_url == None:  #prebuilt resource found in table pb_info
                    file_url = i.pb_info.res_file_path
                    suffix = (file_url).rsplit('.')
                    if suffix[-1]=="mp3" or suffix[-1]=="ogg":
                        output_file = i.pb_info.res_name +"."+suffix[-1]
                    else:
                        output_file = i.pb_info.res_name
                else:
                    file_url = self.urlPrefix + i.download_url
                    output_file = i.name
                output_file = "".join(output_file.split())
                download_path = './'
                print "Audio files: %s" % output_file
                print "type : %s" % i.pb_type.id
                print "audio file_url:%s" % file_url
                ret_val = self.downloadOneFile(file_url, i.pb_type.id,
                                               download_path, output_file)
                if ret_val > 0:
                    print "download success: %s" % output_file
                    tmp = (urllib2.quote(
                        (str(output_file)).replace('/', '')).rsplit('.'))
                    print "tmp:%s" % tmp
                    if (len(tmp) > 1):
                        #if i.prebuilt =='1':
                        crop_output_file = tmp[0] + "_crop_" + str(
                            i.pb_type.id) + "." + tmp[-1]
                        print 'crop output_file: %s' % output_file
                        print "i.crop info: %s" % i.crop
                        if i.crop != None and i.download_url != None:
                            ss, end = i.crop.split(',')
                            ss = int(float(ss))
                            end = int(float(end))
                            duration = end - ss
                            print "ss=%d, duration:%d" % (ss, end)
                            crop_ret = audio_crop(
                                str(output_file), crop_output_file, ss,
                                duration, i.pac, i.download_url, i.crop)
                            print "ss=%d, end crop:%d" % (ss, end)
                            output_file = crop_output_file
                            if crop_ret < 0:
                                return Global.MAKER_DOWNLOADER_STATUS_CROP_ERROR, None
                else:
                    return ret_val, None
                r = {}
                r['fileName'] = urllib2.unquote(str(output_file))
                r['source'] = '1'
                r['fileMd5'] = self.get_md5(str(output_file))
                if i.pb_type.id == Global.MAKER_AUDIO_RINGETONE:
                    r['ringerType'] = "callringtone"
                elif i.pb_type.id == Global.MAKER_AUDIO_UPTONE:
                    r['ringerType'] = "uptone"
                elif i.pb_type.id == Global.MAKER_AUDIO_MESSAGETONE:
                    r['ringerType'] = "messagetone"
                else:
                    print "error"
                    r['ringerType'] = "error"

                r['ringerCode'] = ''
                r['ringerName'] = str(r['fileName']).rsplit(".")[0]
                print "##################### r=", r
                result_list.append(r)

        if len(result_list) <= 0:
            return Global.MAKER_DOWNLOADER_STATUS_2NOTHING, None
        return Global.MAKER_DOWNLOADER_STATUS_SUCCESS, result_list

    def downloadOneFile(self, file_url, file_type, download_path,
                        db_filename=None):
        ret_val = 0
        try:
            print "##################before quote file_url:%s" % file_url
            quote_url = urllib2.quote(str(file_url), ":!?=/[]%")
            print "##################file_url:%s" % file_url
            print ">>>>>>>>>>>>>>>>>>quote_url:%s" % quote_url
            request = urllib2.Request(quote_url)
            print '1:%s' % file_type
            print 'db_filename:%s' % db_filename
            if file_type >= Global.MAKER_BOOTANIMATION_INDEX_START and file_type <= Global.MAKER_BOOTANIMATION_INDEX_END:
                name = 'boot-%d.png' % (
                    file_type - Global.MAKER_BOOTANIMATION_INDEX_START + 1)
            elif file_type in [Global.MAKER_AUDIO_RINGETONE,
                               Global.MAKER_AUDIO_UPTONE,
                               Global.MAKER_AUDIO_MESSAGETONE]:
                name = db_filename
                print "audio file download:%s" % db_filename
            elif file_type in [Global.MAKER_PAPER_LOCKSCREEN,
                               Global.MAKER_PAPER_DESKTOP,
                               Global.MAKER_PAPER_ECARD]:
                print "lock screen file download:%s" % db_filename
                name = db_filename
            else:
                print "new feature waitting ahead...."
                return Global.MAKER_DOWNLOADER_STATUS_2NOTHING
            quote_name = urllib2.quote((str(name)).replace('/', ''))
            print ">>>>>>>>>>>>>>>>>quote_name:%s" % quote_name
            strip_name = "".join((urllib2.unquote(quote_name)).split())
            f = open(download_path + strip_name, 'wb')
            start_time = time.time()
            #print 'time stamp is : ',time.time()
            print start_time
            size = 0
            speed = 0
            data_lines = urllib2.urlopen(request).readlines()
            #data = urllib2.urlopen(request).read()
            for data in data_lines:
                f.write(data)
                size = size + len(data)
                dural_time = float(time.time()) - float(start_time)
                if (dural_time > 0):
                    speed = float(size) / float(dural_time) / (1000 * 1000)
                    while (speed > 1):
                        print 'speed lagger than 1MB/s , sleep(0.1).....'
                        print 'sleep .....'
                        time.sleep(0.1)
                        dural_time = float(time.time()) - float(start_time)
                        speed = float(size) / float(dural_time) / (1000 * 1000)
            print 'total time is : ', dural_time, 'seconds'
            print 'size is       : ', size, 'KB'
            print 'speed is      : ', speed, 'MB/s'
            f.close()
            ret_val = Global.MAKER_DOWNLOADER_STATUS_SUCCESS
        except Exception, e:
            print 'download error: ', e
            return Global.MAKER_DOWNLOADER_STATUS_ERROR
        return ret_val

        # === private util functions...
    def composeBootImgData(self, qs, boot_path, model):
        ret_val = Global.MAKER_DOWNLOADER_STATUS_BOOTIMG_ERROR
        i = 0
        os.chdir(Global.BOOTANIMATION_TMP)
        last = len(qs)
        for obj in qs:
            if obj.pb_type.id < Global.MAKER_BOOTANIMATION_INDEX_START or obj.pb_type.id > Global.MAKER_BOOTANIMATION_INDEX_END:
                last = last - 1
        print 'the last index is %d' % (last)

        try:
            # create a desc.txt
            desc = open('desc.txt', 'w')

            # added at 2015-09-14 - We need auto-adjust the
            # mobile device's screen resolution
#
# FIXME - currently, just hard code here,
#
# in the future, maybe we need take thest
# data from a prebuilt-format, such as DB
            if model != None and model == "M3":
                desc.write('720 1280 24\n')
            else:
                # defult resolution
                desc.write('540 960 24\n')

            for it in range(1, last + 1):
                i += 1
                folder = 'part%d' % (i)
                img = 'boot-%d.png' % (i)
                print ' create %s and -- %s --> %s' \
                        %(folder, img, folder)
                os.mkdir(folder)
                move(img, folder)
                if i == last:
                    line = 'p 0 48 %s\n' % (folder)
                    desc.write(line)
                else:
                    line = 'p 1 48 %s\n' % (folder)
                    desc.write(line)

            desc.close()
            ret_val = Global.MAKER_DOWNLOADER_STATUS_SUCCESS
        except:
            import sys
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
            print 'an exception' + info
            ret_val = Global.MAKER_DOWNLOADER_STATUS_BOOTIMG_ERROR

        os.chdir('../')

        return ret_val

#####################################################################################

    def getAudioFilesList(self):
        r = Rawfiles.objects.filter(pac=self.makerid)
        return r
