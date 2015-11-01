import re
import json

class parser (object):
	def __init__(self):
		f1 = open("listaMarcas.txt","r")
		self.marcas = f1.read().lower().split('\n')

		f2 = open("listaMarcasConErrores.txt","r")
		self.marcasConErrores = f2.read().lower().split('\n')

	def extraerCampos(self,string):
		temp1, marca = self.extraerMarca(string)
		temp2, magnitud, metrica = self.extraerCantidad(temp1)
		nombre, pack = self.extraerPack(temp2)
		return nombre, marca, magnitud, metrica, pack

	def extraerPack(self,string):
		string = string.lower()
		resultadoString = string
		resultadoPack = 1

		res = re.findall(r"x\d+u?", resultadoString)
		if res:
			resultadoPack = max(res, key=len)
			resultadoString = resultadoString.replace(resultadoPack,"").replace("  "," ").strip()
			resultadoPack = int(resultadoPack.replace("u","").replace("x",""))

		return resultadoString, resultadoPack

	def extraerCantidad(self,string):
		log = open("log_de_cantidades_no_registradas.txt", "a")
		cantidadesSinNumero = [" (kg)"," (gr)"," (lt)"," (ml)"," (cc)"]
		cantidadesConNumeroAntes = ["kg","gr","lt","ml","cc"]
		cantidadesEspeciales = ["docena"]

		string = string.lower()
		resultadoString = string
		resultadoCantidad = ""

		# Primero cantidades sin numero
		for c in cantidadesSinNumero:
			if c in string:
				resultadoString = string.replace(c,"").replace("  "," ").strip()
				resultadoCantidad = "1" + c.replace("(","").replace(")","").strip()

		# Cantidades con numero
		for c in cantidadesConNumeroAntes:
			res = re.findall(r"\d*?(?:\.|,|\/)?\d+\s?" + re.escape(c), string)
			if res:
				resultadoCantidad = max(res, key=len)
				resultadoString = string.replace(resultadoCantidad,"").replace("  "," ").strip()
				resultadoCantidad = resultadoCantidad.replace(" ","")

		if resultadoCantidad == "":
			log.write("Cantidad no encontrada: " + resultadoString + '\n')

		resultadoMagnitud, resultadoMetrica = self.normalizarCantidad(resultadoCantidad)

		return resultadoString, resultadoMagnitud, resultadoMetrica

	def normalizarCantidad(self,cantidad):
		# cantidad tiene un string con el siguiente formato: {magnitud}{metrica} o el string vacio
		magnitud = 1
		metrica = ""

		if cantidad is not "":
			res = re.findall(r"\d*(?:\.|,|\/)?\d+", cantidad)
			if res:
				numero = max(res, key=len)
				metrica = cantidad.replace(numero,"")
				if "/" in numero:
					numerador = float(numero.split("/")[0])
					denominador = float(numero.split("/")[1])
					magnitud = numerador / denominador
				else:
					magnitud = float(numero.replace(",","."))

				if "lt" in metrica or "kg" in metrica:
					magnitud = int(magnitud*1000)
					metrica = metrica.replace("kg","gr")
					metrica = metrica.replace("lt","ml")

			# Conversion de cc a ml
			metrica = metrica.replace("cc","ml")

			if isinstance(magnitud, float) and magnitud.is_integer():
				magnitud = int(magnitud)

		return magnitud, metrica
	
	def extraerMarca(self,string):
		log = open("log_de_marcas_no_registradas.txt", "a")
		string = string.lower()
		resultadoString = string
		resultadoMarca = ""

		for marca in self.marcas:
			if re.compile('\s'+marca+'(\s|$)').search(string) is not None:
				resultadoString = re.sub("\s"+marca,"",string) 
				resultadoMarca = marca
				break

		if resultadoMarca == "":
			for marcaConError in self.marcasConErrores:
				marcaMal = marcaConError.split("/")[0].strip().lower()
				marcaBien = marcaConError.split("/")[1].strip().lower()
				if re.compile('\s'+marcaMal+'(\s|$)').search(string) is not None:
					resultadoString = re.sub("\s"+marcaMal,"",string)
					resultadoMarca = marcaBien
					break
				
		if resultadoMarca == "":
			log.write("Marca no encontrada: " + resultadoString + '\n')
		return resultadoString, resultadoMarca


filename = "productosTInglesaSinParsear.json"
archivoNoParseados = open(filename,"r")
productos = json.loads(archivoNoParseados.read())
archivoNoParseados.close()

filename = "productosTInglesaParseados.json"
archivoParseados = open(filename,"w")

productosParseados = []

p = parser()

i = 0

for producto in productos:
	nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto["titulo"])
	prodparseado = {}
	prodparseado["nombre"] = nombre
	prodparseado["marca"] = marca
	prodparseado["metrica"] = metrica
	prodparseado["magnitud"] = magnitud
	prodparseado["packpor"] = pack
	prodparseado["precio"] = producto["precio"]
	productosParseados.append(prodparseado)
	i+=1
	if i == 10:
		break

json.dump(productosParseados,archivoParseados)

# producto = "Galleta La Sin Rival Granetti Snacks x199000 200gr"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))

# print("**********************************")

# producto = "Vino Tinto Santa Teresa Tannat Tetra 1lt"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))

# print("**********************************")

# producto = "Vino Tinto Concha Y Toro Cabernet Sauvignon Reservado 3/4lt"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))

# print("**********************************")

# producto = "Cerveza Stella Artois 0.975lt Pack X3u"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))

# print("**********************************")

# producto = "Chupetin Con Chicle Arcor Big Big Frutilla 600gr"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))

# print("**********************************")

# producto = "Chicle Top Line De Menta Sin Azucar X4u"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))

# print("**********************************")

# producto = "Aderezo Knorr Sabor En Cubos Albahaca Y Ajo 38gr"
# nombre, marca, magnitud, metrica, pack = p.extraerCampos(producto)
# print("Producto: " + producto)
# print("Nombre: " + nombre)
# print("Marca: " + marca)
# print("Magnitud: " + str(magnitud))
# print("Metrica: " + metrica)
# print("Pack: " + str(pack))