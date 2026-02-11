# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksObtainItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()
    price = scrapy.Field()
    subject = scrapy.Field()
    stock = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    UPC = scrapy.Field()
    reviewers = scrapy.Field()
    image = scrapy.Field()
