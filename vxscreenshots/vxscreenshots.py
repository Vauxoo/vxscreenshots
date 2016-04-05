#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

import json
from urllib2 import Request, urlopen
import signal
from os.path import join, isdir, dirname
from os import makedirs
import sqlite3
import logging
from .config import read_config

config = read_config()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class AppShareSmart(object):
    def __init__(self, indicator_id):
        APPINDICATOR_ID = indicator_id
        self.ind_cat = appindicator.IndicatorCategory.SYSTEM_SERVICES
        icon = join(dirname(__file__), 'icon.svg')
        logging.info('Loading icon from %s ' % icon)
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon, self.ind_cat)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.db = config.get('screenshots.database')
        if not isdir(dirname(self.db)):
            makedirs(dirname(self.db))
        logging.info(self.db)
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.get_conn()
        logging.info(config)
        try:
            self.init_db()
        except Exception, e:
            logging.warning(e)
        notify.init(APPINDICATOR_ID)

    def get_conn(self):
        return self.conn.cursor()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE stock_images
                                 (path text, url text, synced boolean)
                            ''')
        self.conn.commit()

    def get_last_three(self):
        elements = self.cursor.execute('''SELECT * FROM stock_images
                                            ORDER BY path
                                            LIMIT 3
                                        ''')
        return elements.fetchone()

    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_joke = gtk.MenuItem('Joke')
        item_last = gtk.MenuItem('Copy Last')
        item_view = gtk.MenuItem('View in Folder')
        item_run = gtk.MenuItem('Run Watcher')
        item_quit.connect('activate', self.quit)
        item_joke.connect('activate', self.joke)
        item_last.connect('activate', self.last)
        item_view.connect('activate', self.view_in_folder)
        item_run.connect('activate', self.run_watcher)
        menu.append(item_last)
        menu.append(item_run)
        menu.append(item_view)
        menu.append(item_joke)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def fetch_joke(self):
        '''Downloading joek this method is just for Test.'''
        request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
        response = urlopen(request)
        joke = json.loads(response.read())['value']['joke']
        return joke

    def quit(self, source):
        notify.uninit()
        gtk.main_quit()

    def run(self):
        logging.info('Serving db: %s' % self.db)
        gtk.main()

    def joke(self, event):
        notify.Notification.new("<b>Joke</b>", self.fetch_joke(), None).show()

    def last(self, event):
        three = self.get_last_three()
        text = three is not None and three[1]
        clipboard = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)
        if text:
            clipboard.set_text(text, -1)
        notify.Notification.new("<b>Copied</b>",
                                'Copied to clipboahd %s' % (text or 'No Image posted yet'), None).show()

    def run_watcher(self, event):
        notify.Notification.new("<b>Watcher is running</b>",
                                'Watcher is running of folder XXXX',
                                None).show()

    def view_in_folder(self, event):
        notify.Notification.new("<b>Folder</b>",
                                'Opening Folder on Explorer', None).show()


def cli():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = AppShareSmart('Shared on S3')
    app.run()

if __name__ == "__main__":
    cli()
