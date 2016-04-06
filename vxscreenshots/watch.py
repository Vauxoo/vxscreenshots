#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from os import makedirs
from os.path import isdir, dirname
import time
import logging
import boto3
import click
import sqlite3
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from .config import read_config
config = read_config()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setFormatter(formatter)

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
        logger.info('Cache dbname: %s' % self.db)
        logger.info('Bucket name: %s' % self.bucket)
        logger.info('Folder name: %s' % self.folder)

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
        logger.info("Screenshot was Modified %s: %s", what, event.src_path)
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
            logger.info("Screenshot was pushed to %s" % self.url)
            self.conn = sqlite3.connect(self.db)
            # Asume if running as a main script it is a dev mode
            self.cursor = self.get_conn()
            try:
                self.init_db()
            except Exception, e:
                logger.warning(e)
            try:
                self.db_insert_new([(event.src_path, self.url, True)])
                logger.warning('Inserted on db %s %s' % (event.src_path,
                                                         self.url))
            except Exception, e:
                logger.warning('I could not insert on cache %s' % e)


@click.option('--path', default=config.get('vxscreenshots.supervised'),
              help='Path to be supervised')
@click.option('--bucket', default=config.get('vxscreenshots.bucket_name'),
              help='Bucket where things will be saved to')
@click.option('--folder', default=config.get('vxscreenshots.folder'),
              help='Inside the bucket how the folder will be named')
@click.command()
def cli(path, bucket, folder):
    '''Watch a folder and push images automatically to amazon S3'''
    event_handler = S3Element(bucket, folder)
    msg = 'Sending to this bucket %s %s %s' % (bucket, folder, path)
    click.echo(msg)
    logger.info(msg)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except IOError:
        logger.info('A crazy file changed')
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
if __name__ == "__main__":
    cli()
