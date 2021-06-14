# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time


class JdSpiPipeline:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
    
    def open_spdier(self,spdier):
        self.start_time = time.time()

    def end_spdier(self,spdier):
        self.end_time = time.time()
        print(self.end_time-self.start_time)

    def process_item(self, item, spider):
        return item
