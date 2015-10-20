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
		# "http://www.devoto.com.uy/acategory.aspx?1725"
		"http://www.devoto.com.uy/acategory.aspx?1194"
		# "http://www.devoto.com.uy/acategory.aspx?1727"
	]
    # Asi es la URL del webservice de las paginas
    # El 5 despues del 4 es el numero de pagina
    # url = "http://www.devoto.com.uy/acategoryonload.aspx?1234,es,4,5,255,,,-1"
	
	rules = (Rule(SgmlLinkExtractor(restrict_xpaths="//ul[@class='subcategorias-lista']/li/a"),
					follow= True,
					callback="parseCategory"),)
    
	def parseCategory(self,response):
	
		# print response.url
					
		url =  response.url.split("%2C") [0]
		for i in range(1, len(response.url.split("%2C"))):
			if i == 3 :
				url +=  "%2C" + str(int(response.url.split("%2C") [i]) + 1)
			else: 
				url += "%2C" + response.url.split("%2C") [i]
				
		if not (response.xpath("//ul[@class='subcategorias-lista']/li/a")):
			if (response.xpath ("//div[@class = 'productos-categoria']")):
				productos = response.xpath("//a[@class='js-fancybox-product fancybox fancybox.iframe']/h2/text()").extract()
				precios = response.xpath("//a[@class='js-fancybox-product fancybox fancybox.iframe']/h3/text()").extract()
				for i in range(0,len(productos)):
					yield Producto(titulo=productos[i].encode('utf-8'), precio=precios[i].encode('utf-8'))
				print "vieja url: " + response.url
				print "nueva url: " + url
				yield Request(url, callback=self.parseCategory, dont_filter=True)
			else:
				print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
			
		# else:     
			# print("encontre cat")

        