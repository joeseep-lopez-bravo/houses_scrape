# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PagesWithRotativeScraperapi1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    distrito= scrapy.Field()
    lugar=scrapy.Field()
    direccion=scrapy.Field()
    pisos = scrapy.Field()
    tamaño = scrapy.Field()
    tipo = scrapy.Field()
    baños = scrapy.Field()
    dormitorios = scrapy.Field()
    precio = scrapy.Field()
    detalle= scrapy.Field()
    cochera = scrapy.Field()
    img= scrapy.Field()
    pass

