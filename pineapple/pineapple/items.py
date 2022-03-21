

from scrapy import Field
from scrapy.item import Item



class PineappleItem(Item):
    product = Field()
    url = Field()
    description = Field()
    sku = Field()
    price = Field()
    currency = Field()
    in_stock = Field()
    size = Field()
    is_new = Field()
    brand = Field()
    spider = Field()
    spider_version = Field()
    timestamp = Field()