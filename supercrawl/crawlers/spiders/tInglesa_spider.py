import scrapy
from scrapy.http import FormRequest
import json
from scrapy.selector import Selector
from crawlers.items import Producto

class tInglesaSpider(scrapy.Spider):
    name = "tInglesa"
    allowed_domains = ["tinglesa.com.uy"]
    start_urls = [
        "http://www.tinglesa.com.uy/categorias.php?idCategoria=1001",
        "http://www.tinglesa.com.uy/categorias.php?idCategoria=1002"
    ]
    categoryTree = {}

    def parse(self,response):
        sel = Selector(text=response.body)
        onclicks = sel.xpath("//td[@class='nivel1']/ul/li/@onclick").extract()
        
        categorias_segundo_nivel = []
        for onclick in onclicks:
            catId = onclick.encode('utf-8').split('\'')[1]
            categorias_segundo_nivel.append(catId)

        categoria_primer_nivel = response.url[54:]
        self.categoryTree[categoria_primer_nivel] = categorias_segundo_nivel
        yield FormRequest("http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php",
                    formdata={'idCategoria': categorias_segundo_nivel[0], 'buscadaDentro': '' , 'number': '500', 'pagina': str(1), 'orden': ''},
                    callback=self.parseCategory)
        
    def parseCategory(self, response):
        current_cat = response.request.body.split("&")[2][12:]
        current_page = int(response.request.body.split("&")[3][7:])

        categorias = []
        for key, value in self.categoryTree.iteritems():
            if current_cat in value:
                categorias = value

        current_cat_index = int(categorias.index(current_cat))

        json_data = json.loads(response.body)
        cantArticulos = int(json_data['resultados'])
        es_ultima_pagina = ((current_page*25) >= cantArticulos)

        sel = Selector(text=json_data.get('filasResultadosListado', ''))
            
        if (sel.xpath ("//div[@class='tabla_subdept']")):
            productos = sel.xpath("//td[@class='descrip_subdept']/a/text()").extract()
            precios = sel.xpath("//td[@align='right']/text()").extract()
            # unidades = sel.xpath("//span[@class='unidad_articulo']/text()").extract()
            for i in range(0,len(productos)):
                yield Producto(titulo=productos[i].encode('utf-8'), precio=precios[i].encode('utf-8'))

        if not es_ultima_pagina:
            yield FormRequest("http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php",
                        formdata={'idCategoria': current_cat, 'buscadaDentro': '' , 'number': '500', 'pagina': str(current_page+1), 'orden': ''},
                        callback=self.parseCategory)
        elif (current_cat_index < len(categorias)-1):
            yield FormRequest("http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php",
                        formdata={'idCategoria': categorias[current_cat_index+1], 'buscadaDentro': '' , 'number': '500', 'pagina': str(1), 'orden': ''},
                        callback=self.parseCategory)

