import scrapy
from scrapy.http import FormRequest

class tInglesaSpider(scrapy.Spider):
    name = "tInglesa"
    allowed_domains = ["tinglesa.com.uy"]
    # start_urls = [
    #     "http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php"
    # ]

    def start_requests(self):
        return [ FormRequest("http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php",
                     formdata={'idCategoria': '78', 'buscadaDentro': '' , 'number': '50', 'pagina': '2', 'orden': ''},
                     callback=self.parse) ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)