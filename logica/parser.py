
f = open("listaMarcas.txt","r")
marcas = f.readlines()

def extraerCantidad(string):
	log = open("log_de_cantidades_no_registradas.txt", "a")
	cantidadesSinNumero = [" (kg)"," (gr)"," (lt)"," (ml)"," (cc)"]
	cantidadesConNumeroAntes = ["kg","gr","lt","ml","cc"]

	string = string.lower()

	# Primero cantidades sin numero
	for c in cantidadesSinNumero:
		if c in string:
			resultadoString = string.replace(c,"").replace("  "," ").strip()
			resultadoCantidad = "1" + c.replace("(","").replace(")","").strip()
			return resultadoString, resultadoCantidad

producto = "Galleta La Sin Rival Granetti Snacks (lt)"
tituloSinCantidad, cantidad = extraerCantidad(producto)
print("Titulo: " + tituloSinCantidad + "\n")
print("Cantidad: " + cantidad + "\n")

def extraerMarca(string, marcas):
	log = open("log_de_marcas_no_registradas.txt", "a")
	string = string.lower()
	resultadoString = string
	resultadoMarca = ""
	for marca in marcas:
		marca = marca.lower().replace('\n','')
		if marca in string:
			palabrasString = set(string.split())
			palabrasMarca = set(marca.split())
			if palabrasMarca.issubset(palabrasString):
				resultadoMarca = marca
				resultadoString = string.replace(marca,"").replace("  "," ").strip()
				break
			# Esta solucion no contempla un caso como el siguiente
			# Producto: "Alfajor Rival La Sin Rivales"
			# Marca: "La Sin Rival"
			# Pero no tengo ganas de pensar casos TAN PERO TAN PERO TAN bordes
	if resultadoMarca == "":
		log.write("Marca no encontrada: " + resultadoString + '\n')
	return resultadoString, resultadoMarca

producto = "Galleta La Sin Rival Granetti Snacks 200gr"
tituloSinMarca, marca = extraerMarca(producto,marcas)
print("Titulo: " + tituloSinMarca + "\n")
print("Marca: " + marca + "\n")

