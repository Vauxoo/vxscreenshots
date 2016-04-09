# -*- coding: UTF-8 -*-
'''
Following this strategy_ we simply go to the 

.. _strategy: http://askubuntu.com/questions/48321/how-do-i-start-applications-automatically-on-login
'''
from os.path import dirname, join, expanduser
from os import listdir
from shutil import copy2

HOME = expanduser("~")

class Configure(object):
    def __init__(self):
        self.shutter = False
        self.vxssicon = False
        self.vxsswatcher = False

    def set_startup(self):
        origin = join(dirname(__file__), 'config', 'autostart')
        dest = join(HOME, '.config')
        for o in listdir(origin):
            print o
            # copy2(o, dest)
