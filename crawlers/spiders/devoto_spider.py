import scrapy
from scrapy.http import FormRequest
import json
from scrapy.selector import Selector
from scrapy.spiders import Rule, CrawlSpider
from crawlers.items import Producto
from scrapy.linkextractors.sgml import SgmlLinkExtractor

class devotoSpider(CrawlSpider):
	name = "devoto"
	allowed_domains = ["devoto.com.uy"]
	start_urls = [
		"http://www.devoto.com.uy/acategory.aspx?1725"
	]
    # Asi es la URL del webservice de las paginas
    # El 5 despues del 4 es el numero de pagina
    # url = "http://www.devoto.com.uy/acategoryonload.aspx?1234,es,4,5,255,,,-1"
	
	rules = (Rule(SgmlLinkExtractor(restrict_xpaths="//ul[@class='subcategorias-lista']/li/a"),
                  follow= True,
                  callback="parseCategory"),)
    
	def parseCategory(self,response):
        if not (response.xpath("//ul[@class='subcategorias-lista']/li/a")):
            print("encontre pagina con productos")
        else:
            print("encontre cat")
