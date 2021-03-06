import scrapy
from scrapy.http import FormRequest
import json
from scrapy.selector import Selector
from scrapy.spiders import Rule, CrawlSpider
from crawlers.items import Producto
from scrapy.http import Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor

class devotoSpider(CrawlSpider):
	name = "devoto"
	allowed_domains = ["devoto.com.uy"]
	start_urls = [
		"http://www.devoto.com.uy/acategory.aspx?1725",
		"http://www.devoto.com.uy/acategory.aspx?1154",
		"http://www.devoto.com.uy/acategory.aspx?1155",
		"http://www.devoto.com.uy/acategory.aspx?1162",
		"http://www.devoto.com.uy/acategory.aspx?1180"
	]

	
	rules = (Rule(SgmlLinkExtractor(restrict_xpaths="//ul[@class='subcategorias-lista']/li/a"),
					follow= True,
					callback="parseCategory"),)
	
	def parseCategory(self,response):
	
		# print response.url
		aux = response.url.replace("%2C", ",")
		url =  aux.split(",") [0]
		for i in range(1, len(aux.split(","))):
			if i == 3 :
				url +=  "," + str(int(aux.split(",") [i]) + 1)
			else: 
				url += "," + aux.split(",") [i]
				
		if not (response.xpath("//ul[@class='subcategorias-lista']/li/a")):
			if (response.xpath ("//div[@class = 'productos-categoria']")):
				productos = response.xpath("//a[@class='js-fancybox-product fancybox fancybox.iframe']/h2/text()").extract()
				precios = response.xpath("//a[@class='js-fancybox-product fancybox fancybox.iframe']/h3/text()").extract()
				for i in range(0,len(productos)):
					titulo = productos[i].encode('utf-8')
					precio = precios[i].encode('utf-8')
					yield Producto(titulo=titulo, precio=precio)
				yield Request(url, callback=self.parseCategory, dont_filter=True)

			
		