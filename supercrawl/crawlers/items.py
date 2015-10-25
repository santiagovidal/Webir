# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Producto(scrapy.Item):
	nombre = scrapy.Field()
	marca = scrapy.Field()
	magnitud = scrapy.Field()
	metrica = scrapy.Field()
	packpor = scrapy.Field()
	precio = scrapy.Field()
	pass
