#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
from os import makedirs
from os.path import isdir, dirname
import time
import logging
import boto3
import sqlite3
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from .config import read_config
config = read_config()


class S3Element(LoggingEventHandler):

    def __init__(self, bucket, folder):
        super(LoggingEventHandler, self).__init__()
        self.folder = folder
        self.bucket = bucket
        self.url = ''
        self.valid_ext = ['.png', '.jpg', '.gif', '.jpeg']
        self.db = config.get('vxscreenshots.database')
        if not isdir(dirname(self.db)):
            makedirs(dirname(self.db))
        logging.info('Cache dbname: %s' % self.db)
        logging.info('Bucket name: %s' % self.bucket)
        logging.info('Folder name: %s' % self.folder)

    def get_conn(self):
        return self.conn.cursor()

    def get_path(self, src_path):
        return '{}/{}'.format(self.folder, src_path)

    def get_url(self, fname):
        return "http://{bucket}/{fname}".format(bucket=self.bucket,
                                                fname=fname)

    def init_db(self):
        self.cursor.execute('''CREATE TABLE stock_images
                                 (path text, url text, synced boolean)
                            ''')

    def db_insert_new(self, images):
        self.cursor.executemany('INSERT INTO stock_images VALUES (?,?,?)',
                                images)
        self.conn.commit()

    def on_modified(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.send_to_s3(what, event)

    def send_to_s3(self, what, event):
        logging.info("Screenshot was Modified %s: %s", what, event.src_path)
        name, ext = os.path.splitext(event.src_path)
        if what != 'directory' and \
           os.path.isfile(event.src_path) and \
           ext in self.valid_ext:
            s3 = boto3.resource('s3')
            data = open(event.src_path, 'rb')
            fname = self.get_path(os.path.basename(data.name))
            bucket = s3.Bucket(self.bucket)
            bucket.put_object(Key=fname, Body=data, ACL='public-read',
                              ContentType='image/%s' % ext[1:])
            self.url = self.get_url(fname)
            logging.info("Screenshot was pushed to %s" % self.url)
            self.conn = sqlite3.connect(self.db)
            # Asume if running as a main script it is a dev mode
            self.cursor = self.get_conn()
            try:
                self.init_db()
            except Exception, e:
                logging.warning(e)
            try:
                self.db_insert_new([(event.src_path, self.url, True)])
                logging.warning('Inserted on db %s %s' % (event.src_path,
                                                          self.url))
            except Exception, e:
                logging.warning('I could not insert on cache %s' % e)


def cli():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # TODO: convert to click commands
    if '--help' in sys.argv:
        print '''usage: command [path to watch] [amazon bucket] [folder in bucket]
If no arg provided it will read values on user config file
on ~/.vxscreenshots/vxscreenshots.ini'''
        exit()
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    bucket = sys.argv[2] if len(sys.argv) > 2 else ''
    folder = sys.argv[3] if len(sys.argv) > 3 else ''
    event_handler = S3Element(bucket or config.get('vxscreenshots.bucket_name'),
                              folder or config.get('vxscreenshots.folder'))
    observer = Observer()
    if path == '.':
        path = config.get('vxscreenshots.supervised')
    logging.info('Watching this Folder: %s' % path)
    if not isdir(path):
        makedirs(path)
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except IOError:
        logging.info('A crazy file changed')
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
if __name__ == "__main__":
    cli()
