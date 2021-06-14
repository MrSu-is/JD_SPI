# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_detail = scrapy.Field()
    price_detail = scrapy.Field()
    #picture = scrapy.Field()
    shop_detail = scrapy.Field()
    brand = scrapy.Field()
    goods_id = scrapy.Field()
    pass
