# coding:cp936  
# Zfile.py  
# xxteach.com  
import zipfile   
import os.path   
import os
import md5
   
class ZFile(object):   
    def __init__(self, filename, mode='r', basedir='',compression=zipfile.ZIP_STORED):   
        self.filename = filename
        self.mode = mode   
        if self.mode in ('w', 'a'):   
            self.zfile = zipfile.ZipFile(filename, self.mode, compression)   
        else:   
            self.zfile = zipfile.ZipFile(filename, self.mode)   
        self.basedir = basedir   
        if not self.basedir:   
            self.basedir = os.path.dirname(filename)
    def get_md5(self, full_filename):
        f=file(full_filename,'rb')
        return md5.new(f.read()).hexdigest()
    def adddir(self):
        for parent,dirnames,filenames in os.walk(self.basedir):
            for filename in filenames:
                self.addfile(os.path.join(parent, filename))
    def addfile(self, path, arcname=None):   
        path = path.replace('//', '/')   
        if not arcname:   
            if path.startswith(self.basedir):   
                arcname = path[len(self.basedir):]   
            else:   
                arcname = ''   
        self.zfile.write(path, arcname)   
              
    def addfiles(self, paths):   
        for path in paths:   
            if isinstance(path, tuple):   
                self.addfile(*path)   
            else:   
                self.addfile(path)   
              
    def close(self):   
        self.zfile.close()   
          
    def extract_to(self, path):   
        for p in self.zfile.namelist():   
            self.extract(p, path)   
              
    def extract(self, filename, path):   
        if not filename.endswith('/'):   
            f = os.path.join(path, filename)   
            dir = os.path.dirname(f)   
            if not os.path.exists(dir):   
                os.makedirs(dir)   
            file(f, 'wb').write(self.zfile.read(filename))   
              
          
#def create(zfile, files):   
#    z = ZFile(zfile, 'w')   
#    z.addfiles(files)   
#    z.close()   
      
#def extract(zfile, path):   
#    z = ZFile(zfile)   
#    z.extract_to(path)   
#    z.close() 

#create("aa.zip", ["bootanimation"])
