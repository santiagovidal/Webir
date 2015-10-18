import scrapy
from scrapy.http import FormRequest
import json
from scrapy.selector import Selector
from crawlers.items import Producto

class tInglesaSpider(scrapy.Spider):
    name = "devoto"
    allowed_domains = ["devoto.com.uy"]
    start_urls = [
        
    ]
    # Asi es la URL del webservice de las paginas
    # El 5 despues del 4 es el numero de pagina
    url = "http://www.devoto.com.uy/acategoryonload.aspx?1234,es,4,5,255,,,-1"

    def parse(self,response):

        
    def parseCategory(self, response):
