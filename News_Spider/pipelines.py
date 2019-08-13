# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
import datetime

date=datetime.date.today()
class NewsSpiderPipeline(object):

    def __init__(self):
        # connecting to mongodb server
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['NewsDB']
        self.collection = db['Articles{}'.format(date)]   # making collection

    def process_item(self, item, spider):

        logging.info("News headline and complete article being stored in database")
        self.collection.insert(dict(item))    # inserting items to mongodb collection
        return item




