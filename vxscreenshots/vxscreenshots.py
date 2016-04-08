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
from contextlib import closing

config = read_config()


class AppShareSmart(object):
    def __init__(self, indicator_id):
        APPINDICATOR_ID = indicator_id
        self.ind_cat = appindicator.IndicatorCategory.SYSTEM_SERVICES
        self.format_logging()
        icon = join(dirname(__file__), 'icon.svg')
        self.logger.info('Loading icon from %s ' % icon)
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                                    icon,
                                                    self.ind_cat)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.db = config.get('vxscreenshots.database')
        if not isdir(dirname(self.db)):
            makedirs(dirname(self.db))
        self.logger.info(self.db)
        self.conn = sqlite3.connect(self.db)
        try:
            self.init_db()
        except Exception, e:
            self.logger.warning(e)
        notify.init(APPINDICATOR_ID)

    def format_logging(self, log_level='INFO'):
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)
                logging.basicConfig(format='%(asctime)s: %(name)s: '
                                    '%(levelname)s: %(message)s',
                                    level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def init_db(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute('''CREATE TABLE stock_images
                                    (path text,
                                     url text,
                                     synced boolean,
                                     dt datetime default current_timestamp)
                           ''')
            self.conn.commit()

    def get_last_three(self):
        with closing(self.conn.cursor()) as cursor:
            elements = cursor.execute('''SELECT * FROM stock_images
                                         ORDER BY dt desc
                                         LIMIT 3
                                      ''')
            return elements.fetchone()

    def build_menu(self):
        menu = gtk.Menu()
        item_last = gtk.MenuItem('Get Image code Last Item')
        item_last_link = gtk.MenuItem('Direct Link')
        item_last_html = gtk.MenuItem('Html')
        item_last_md = gtk.MenuItem('Markdown')
        item_last_rst = gtk.MenuItem('rST')
        item_quit = gtk.MenuItem('Quit')
        item_joke = gtk.MenuItem('Joke')
        item_view = gtk.MenuItem('View in Folder')
        separator = gtk.SeparatorMenuItem()
        separator_m = gtk.SeparatorMenuItem()
        separator_q = gtk.SeparatorMenuItem()
        item_run = gtk.MenuItem('Run Watcher')
        item_last_link.connect('activate', self.last_link)
        item_last_html.connect('activate', self.last_html)
        item_last_md.connect('activate', self.last_md)
        item_last_rst.connect('activate', self.last_rst)
        item_quit.connect('activate', self.quit)
        item_joke.connect('activate', self.joke)
        item_view.connect('activate', self.view_in_folder)
        item_run.connect('activate', self.run_watcher)
        subMenu = gtk.Menu()
        subMenu.append(item_last_link)
        subMenu.append(item_last_html)
        subMenu.append(item_last_md)
        subMenu.append(item_last_rst)
        item_last.set_submenu(subMenu)
        menu.append(item_last)
        menu.append(separator_m)
        menu.append(item_run)
        menu.append(item_view)
        menu.append(separator)
        menu.append(item_joke)
        menu.append(separator_q)
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
        self.logger.info('Serving db: %s' % self.db)
        gtk.main()

    def joke(self, event):
        notify.Notification.new("<b>Joke</b>", self.fetch_joke(), None).show()

    def clipboard(self, text):
        clipboard = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)
        if text:
            clipboard.set_text(text, -1)
        self.logger.info(text)
        msg = 'Copied to clipboard %s' % (text or 'No Image posted yet')
        notify.Notification.new('<b>Copied</b>', msg, None).show()

    def last_link(self, event):
        link = self.last(event)
        self.clipboard(link)

    def last_html(self, event):
        link = self.last(event)
        self.clipboard('<img src="%s" width=auto></img>' % link)

    def last_md(self, event):
        link = self.last(event)
        self.clipboard('![](%s)' % link)

    def last_rst(self, event):
        link = self.last(event)
        self.clipboard(''
                       '.. image:: %s\n'
                       '   :height: 100\n'
                       '   :width: 100\n'
                       '   :scale: 100\n'
                       '   :alt: alternate text' % link)

    def last(self, event):
        three = self.get_last_three()
        return three is not None and three[1]

    def run_watcher(self, event):
        notify.Notification.new("<b>Watcher is running</b>",
                                'Running screenshot.sh script and sending \n'
                                'screenshots to configured watched image....',
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
