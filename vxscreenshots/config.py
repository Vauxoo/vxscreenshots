# -*- coding: UTF-8 -*-

import os
import ConfigParser
from os.path import dirname, join, expanduser, isdir, isfile
HOME = expanduser("~")


try:
    import pwd
except ImportError:
    import getpass
    pwd = None


def current_user():
    if pwd:
        return pwd.getpwuid(os.geteuid()).pw_name
    else:
        return getpass.getuser()


def get_template_config(cfg):
    dirconfig = dirname(cfg)
    content = '''[vxscreenshots]
database={dirconfig}
supervised={supervised}
folder={username}
bucket_name={bucket}
    '''.format(dbconfig=dirconfig,
               supervised=join(HOME, 'Pictures', 'screenshots'),
               username=current_user(),
               bucket='screenshots.yourdomain.com')
    return content


def read_config():
    cfg = os.path.join(HOME,
                       '.vxscreenshots',
                       'vxscreenshots.ini')
    if not isfile(cfg) and not isdir(dirname(cfg)):
        os.makedirs(dirname(cfg))
        with open(cfg, 'a+') as configfile:
            configfile.write(get_template_config(cfg))
    parser = ConfigParser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv
