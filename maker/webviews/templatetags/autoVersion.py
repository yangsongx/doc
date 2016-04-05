from django import template
import utils
import Global
register = template.Library()
import os, re, sys
from shutil import copy

version_cache = {}

rx = re.compile(r"^(.*)\.(.*?)$")


def auto_version(path_string):
    if utils.is_ksyun_server() == None:
        return path_string
    try:
        if path_string in version_cache:
            mtime = version_cache[path_string]
        else:
            mtime = os.path.getmtime('%s%s' % (Global.AUTO_VERSION_STATCI_PATH,
                                               path_string, ))
            version_cache[path_string] = mtime
        v_str = rx.sub(r"\1.%d.\2" % mtime, path_string)
        return v_str
    except:
        return path_string


register.simple_tag(auto_version)
