#coding:utf-8
import os
import codecs
import Global
from Download import Downloader
from shutil import move, rmtree, copy
from xml.dom import minidom as xml
from models import Rawfiles
from models import PbType

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ManiFest:
    def __init__(self, maker_id):
        self.makerid = maker_id
        self.verCode = "0.0.1"
        self.minSdkVer = '17'
        self.model = None
        self.description = None

        self.dom = None
        self.root = None
        self.writer = None
        self.impl = None

    def makeEasyTag(self, dom, tagname, value, type='text'):
        tag = dom.createElement(tagname)
        if value.find(']]>') > -1:
            type = 'text'
        if type == 'text':
            value = value.replace('&', '&amp;')
            value = value.replace('<', '&lt;')
            text = dom.createTextNode(value)
        elif type == 'cdata':
            text = dom.createCDATASection(value)
        tag.appendChild(text)
        return tag

    def createManifest(self):
        return None

    def createItem(self, itemName, itemContent):
        item = None
        if self.dom != None:
            item = self.makeEasyTag(self.dom, itemName, itemContent, 'text')
        return item

    def createGlobalItems(self, verCode, minSdkVer, model, desc):
        item_ver = self.makeEasyTag(self.dom, "verCode", verCode, "text")
        self.root.appendChild(item_ver)
        item_minSDK = self.makeEasyTag(self.dom, "minSdkVer", minSdkVer,
                                       "text")
        self.root.appendChild(item_minSDK)
        item_model = self.makeEasyTag(self.dom, "model", model, "text")
        self.root.appendChild(item_model)
        item_desc = self.makeEasyTag(self.dom, "description", desc, "text")
        self.root.appendChild(item_desc)
        self.model = model

    def prepareWriter(self):
        isExists = os.path.exists(str(self.makerid))
        if not isExists:
            os.mkdir(str(self.makerid))
        else:
            rmtree(str(self.makerid))
            os.mkdir(str(self.makerid))
            print "dir already exists:%s" % self.makerid
        os.chdir(str(self.makerid))
        self.impl = xml.getDOMImplementation()
        self.dom = self.impl.createDocument(None, "manifest", None)

        self.root = self.dom.documentElement

        #self.root.appendChild(item)
        self.fd = file('manifest', 'w')
        self.writer = codecs.lookup('utf-8')[3](self.fd)

    def writeManifest(self):
        print "XXXXXXXXwrite manifest"
        if self.dom != None and self.writer != None:
            print "##############write manifest"
            self.dom.writexml(self.writer, '', '    ', '\n', 'utf-8')

    def colseWriter(self):
        if self.writer != None:
            self.writer.close()


class Ringer:
    def __init__(self, mid, manifest):
        self.maker_id = mid
        self.manifest = manifest
        self.root = manifest.root
        self.dom = manifest.dom
        self.ringerList = None
        self.downloadStatus = -100

    def createRingerNode(self):
        return None

    def get_md5(self, full_filename):
        f = file(full_filename, 'rb')
        return md5.new(f.read()).hexdigest()
    # This util handling would included:
    # o  download all audio file(in Download class)
    # o  create manifest
    def handlingRingtone(self):
        downloader = Downloader(self.maker_id, Global.QINIU_DOWNLOAD_PREFIX)
        self.downloadStatus, self.ringerList = downloader.downloadAllfiles(
            Global.RESOURCE_TYPE_RINGER, self.manifest.model)
        print 'get ringer list', self.ringerList
        # After get all files, record them into a DB
        self.recordIntoManifest()
        print 'return the func'
        return self.downloadStatus, self.ringerList

    def recordIntoManifest(self):
        if self.ringerList == None:
            return None
        if self.ringerList == -1:
            return -1
        if len(self.ringerList) > 0:
            self.ringgerRoot = self.manifest.makeEasyTag(
                self.dom, "moduleRinger", "", "text")
            self.root.appendChild(self.ringgerRoot)
            ringer_ids = 0
        for i in self.ringerList:
            if self.manifest != None:
                ringer_id = self.manifest.makeEasyTag(self.dom, "ringer", "",
                                                      "text")
                self.ringgerRoot.appendChild(ringer_id)
                rid = self.manifest.makeEasyTag(self.dom, "id",
                                                str(ringer_ids), "text")
                ringer_ids += 1

                ringer_id.appendChild(rid)
                s = self.manifest.makeEasyTag(self.dom, "source", i['source'],
                                              "text")
                ringer_id.appendChild(s)
                fn = self.manifest.makeEasyTag(self.dom, "fileName",
                                               i['fileName'], "text")
                ringer_id.appendChild(fn)
                fm = self.manifest.makeEasyTag(self.dom, "fileMd5",
                                               i['fileMd5'], "text")
                ringer_id.appendChild(fm)
                rt = self.manifest.makeEasyTag(self.dom, "ringerType",
                                               i['ringerType'], "text")
                ringer_id.appendChild(rt)
                rc = self.manifest.makeEasyTag(self.dom, "ringerCode",
                                               i['ringerCode'], "text")
                ringer_id.appendChild(rc)
                rn = self.manifest.makeEasyTag(self.dom, "ringerName",
                                               i['ringerName'], "text")
                ringer_id.appendChild(rn)
        #self.manifest.writeManifest()
        #self.manifest.colseWriter()

        return 0


class Wllpaper:
    def __init__(self, maker_id, root, dom, writer):
        self.source = ''
        self.fileName = ''
        self.fileMd5 = ''
        self.paperType = ''
        self.paperCode = ''
        self.paperName = ''

        self.maker_id = maker_id
        self.root = root
        self.dom = dom
        self.writer = writer


class Bootanimation:
    def __init__(self, maker_id, manifest=None):
        self.source = ''
        self.fileName = ''
        self.fileMd5 = ''
        self.bootCode = ''
        self.BootName = ''
        self.maker_id = maker_id
        if manifest != None:
            self.root = manifest.root
            self.dom = manifest.dom
            self.writer = manifest.writer
        self.manifest = manifest
        self.bootAnimateRoot = None

    def getAnimationFiles(self):
        downloader = Downloader(self.maker_id, Global.QINIU_DOWNLOAD_PREFIX)
        return downloader.downloadAllfiles(Global.RESOURCE_TYPE_ANIMATION,
                                           self.manifest.model)

    def createBootManifestItems(self, source, fileName, fileMd5, bootCode,
                                bootName):
        if self.manifest != None:
            self.bootAnimateRoot = self.manifest.makeEasyTag(
                self.dom, "moduleBootanim", "", "text")
            self.root.appendChild(self.bootAnimateRoot)

            s = self.manifest.makeEasyTag(self.dom, "source", source, "text")
            self.bootAnimateRoot.appendChild(s)
            fn = self.manifest.makeEasyTag(self.dom, "fileName", fileName,
                                           "text")
            self.bootAnimateRoot.appendChild(fn)
            fm = self.manifest.makeEasyTag(self.dom, "fileMd5", fileMd5,
                                           "text")
            self.bootAnimateRoot.appendChild(fm)
            bc = self.manifest.makeEasyTag(self.dom, "bootCode", bootCode,
                                           "text")
            self.bootAnimateRoot.appendChild(bc)
            bn = self.manifest.makeEasyTag(self.dom, "bootName", bootName,
                                           "text")
            self.bootAnimateRoot.appendChild(bn)

            # below 2 lines SHOULD be called by the last one, comment them
            # as ringtone followed with bootanimation
            #self.manifest.writeManifest()
            #self.manifest.colseWriter()

    def constructBootanimation(self):
        os.mkdir("bootanimation")
        os.chdir("bootanimation")
        for i in range(0, 12):
            os.mkdir("part" + str(i))
            move("../" + Global.BOOTANIMATION_TMP + "part" + str(i) + ".*",
                 "part" + str(i))


#####################################################################################
class LockScreen:
    def __init__(self, mid, manifest):
        self.maker_id = mid
        self.manifest = manifest
        self.root = manifest.root
        self.dom = manifest.dom
        self.paperList = None
        self.downloadStatus = -100

    def createManifestItems(self):
        if self.paperList == None:
            return None
        if self.paperList == -1:
            return -1

        if len(self.paperList) > 0:
            self.wallpaperRoot = self.manifest.makeEasyTag(
                self.dom, "moduleWallpaper", "", "text")
            self.root.appendChild(self.wallpaperRoot)
            wallpapers_ids = 0
        for i in self.paperList:
            if self.manifest != None:
                paper_root = self.manifest.makeEasyTag(self.dom, "wallpaper",
                                                       "", "text")
                self.wallpaperRoot.appendChild(paper_root)
                rid = self.manifest.makeEasyTag(self.dom, "id",
                                                str(wallpapers_ids), "text")
                wallpapers_ids += 1
                paper_root.appendChild(rid)
                fn = self.manifest.makeEasyTag(self.dom, "fileName",
                                               i['fileName'], "text")
                paper_root.appendChild(fn)
                fm = self.manifest.makeEasyTag(self.dom, "fileMd5",
                                               i['fileMd5'], "text")
                paper_root.appendChild(fm)
                pt = self.manifest.makeEasyTag(self.dom, "paperType",
                                               i['paperType'], "text")
                paper_root.appendChild(pt)
                pn = self.manifest.makeEasyTag(self.dom, "paperName",
                                               i['paperName'], "text")
                paper_root.appendChild(pn)
    #################################################################################
    def handlingLockScreen(self):
        downloader = Downloader(self.maker_id, Global.QINIU_DOWNLOAD_PREFIX)
        self.downloadStatus, self.paperList = downloader.downloadAllfiles(
            Global.RESOURCE_TYPE_PAPER, self.manifest.model)
        self.createManifestItems()
        return self.downloadStatus, self.paperList


#####################################################################################
class AppItem:
    def __init__(self, mid, manifest):
        self.maker_id = mid
        self.manifest = manifest
        self.root = manifest.root
        self.dom = manifest.dom

    #################################################################################
    def handlingAppItem(self):
        queryset = Rawfiles.objects.filter(
            pac=self.maker_id,
            pb_type=PbType(id=Global.MAKER_TYPE_APP))
        if len(queryset) == 0:
            print 'no app specified, ignore'
            # FIXME as we decide AppItem is the last entry, DO NOT
            # Forget to close the manifest writing job
            self.manifest.writeManifest()
            self.manifest.colseWriter()
            return 0

        print 'Totally %d app defined in DB' % (len(queryset))
        id = 1
        app_root = self.manifest.makeEasyTag(self.dom, 'moduleApp', '', 'text')
        self.root.appendChild(app_root)
        for it in queryset:
            print 'write the %d items...' % (id)
            s = self.dom.createElement('appItem')
            s.setAttribute('humanName', '')
            s.setAttribute('pkgName', it.name)
            s.setAttribute('appVerCode', '')
            id += 1
            app_root.appendChild(s)

        #TODO code , will try write the XML
        self.manifest.writeManifest()
        self.manifest.colseWriter()
        return 0
