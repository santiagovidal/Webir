import json
from busqueda2 import Busqueda
with open("../supercrawl/crawlers/productosDevotoParseados.json","r") as archivo_datos: 
	datos = json.loads(archivo_datos.read())
	datos = Busqueda().obtenerMejores(datos,10)
	#datos = datos[0].items()
	print(datos)
print datos