import json
from busqueda import Busqueda

opcion = -1
while opcion != 0:
	print 
	corpus = int(input("Corpus? [0:Tinglesa, 1:Devoto] "))
	if corpus == 0: 
		with open("../supercrawl/crawlers/productosTInglesaParseados.json","r") as archivo_datos: 
			datos = json.loads(archivo_datos.read())
	elif corpus == 1:
		with open("../supercrawl/crawlers/productosDevotoParseados.json","r") as archivo_datos: 
			datos = json.loads(archivo_datos.read())
	else: continue
	print "\n\n*********************************************"
	print "0: Salir"
	print "1: Desarmando packpor & magnitud"
	print "2: Desarmando solo magnitud"
	print "3: Desarmando solo packpor"
	print "4: Sin desarmar"
	print ""
	print "Ingrese una opcion"
	opcion = int(input("> "))
	if opcion == 0: continue
	cantidad = int(input("Cantidad: "))
	if opcion == 1:
		quiero_magnitud = int(input("Magnitud: "))
		quiero_packpor  = int(input("Packpor : "))
		datos = Busqueda().obtenerMejores(datos,cantidad,quiero_magnitud=quiero_magnitud,quiero_packpor=quiero_packpor)
	elif opcion == 2:
		quiero_magnitud = int(input("Magnitud: "))
		datos = Busqueda().obtenerMejores(datos,cantidad,quiero_magnitud=quiero_magnitud)
	elif opcion == 3:
		quiero_packpor = int(input("Packpor : "))
		datos = Busqueda().obtenerMejores(datos,cantidad,quiero_packpor=quiero_packpor)
	elif opcion == 4:
		datos = Busqueda().obtenerMejores(datos,cantidad)
	k=1
	for dato in datos:
		print "************** Producto ",k," **************"
		print "Nombre          : ", dato["nombre"]
		print "Marca           : ", dato["marca"] 
		print "Metrica         : ", dato["metrica"]
		print "Magnitud        : ", dato["magnitud"]
		print "UnidadWeb       : ", dato["unidadWeb"]
		print "Packpor         : ", dato["packpor"] 
		print "Cantidad        : ", dato["cantidad"]
		print "Precio unitario : ", dato["precio"]
		k += 1