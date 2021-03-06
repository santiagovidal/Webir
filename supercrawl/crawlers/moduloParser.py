import re
import json

class parser (object):
	def __init__(self, rutaCarpeta=""):
		f1 = open(rutaCarpeta + "listaMarcas.txt","r")
		self.marcas = f1.read().split('\n')

		f2 = open(rutaCarpeta + "listaMarcasConErrores.txt","r")
		self.marcasConErrores = f2.read().lower().split('\n')

	def parsearJSON(self, filename, filenameNuevo):
		archivoNoParseados = open(filename,"r")
		productos = json.loads(archivoNoParseados.read())
		archivoNoParseados.close()

		archivoParseados = open(filenameNuevo,"w")
		archivoParseados.write("[")

		i = 0
		for producto in productos:
			i += 1
			print("Parseando: " + producto["titulo"] + "\n")
			nombre, marca, magnitud, metrica, unidadWeb, pack = self.extraerCampos(producto["titulo"])
			precio = self.parsearPrecio(producto["precio"])
			prodparseado = {}
			prodparseado["nombre"] = nombre
			prodparseado["marca"] = marca
			prodparseado["metrica"] = metrica
			prodparseado["unidadWeb"] = unidadWeb
			prodparseado["magnitud"] = magnitud
			prodparseado["packpor"] = pack
			prodparseado["precio"] = precio
			json.dump(prodparseado,archivoParseados)
			if i < len(productos):
				archivoParseados.write(",\n")

		archivoParseados.write("]")



	def extraerCampos(self,string):
		temp1, marca = self.extraerMarca(string)
		temp2, magnitud, metrica, unidadWeb = self.extraerCantidad(temp1)
		nombre, pack = self.extraerPack(temp2)
		return nombre, marca, magnitud, metrica, unidadWeb, pack

	def extraerPack(self,string):
		string = string.lower()
		resultadoString = string
		resultadoPack = 1

		res = re.findall(r"x\s?\d+u?", resultadoString)
		if res:
			resultadoPack = max(res, key=len)
			resultadoString = resultadoString.replace(resultadoPack,"")
			resultadoPack = int(resultadoPack.replace("u","").replace("x","").replace(" ",""))

		return resultadoString.replace("  "," ").strip(), resultadoPack

	def extraerCantidad(self,string):
		log = open("log_de_cantidades_no_registradas.txt", "a")
		cantidadesSinNumero = [" (kg)"," (gr)"," (lt)"," (ml)"," (cc)", "el kg", "x kg"]
		cantidadesConNumeroAntes = ["kg","gr","lt","ml","cc", "k", "g", "l"]
		cantidadesEspeciales = ["docena"]

		string = string.lower()
		resultadoString = string
		resultadoCantidad = ""

		# Primero cantidades sin numero
		for c in cantidadesSinNumero:
			if c in string:
				resultadoString = string.replace(c,"")
				c = c.replace("el","").replace("x","")
				resultadoCantidad = "1" + c.replace("(","").replace(")","").strip()

		# Cantidades con numero
		for c in cantidadesConNumeroAntes:
			res = re.findall(r"\d*?(?:\.|,|\/)?\d+\s?" + re.escape(c), string)
			if res:
				resultadoCantidad = max(res, key=len)
				resultadoString = string.replace(resultadoCantidad,"")
				resultadoCantidad = resultadoCantidad.replace(" ","")
				break

		if resultadoCantidad == "":
			log.write("Cantidad no encontrada: " + resultadoString.encode('utf-8') + '\n')

		resultadoMagnitud, resultadoMetrica, unidadWeb = self.normalizarCantidad(resultadoCantidad)

		# Le saco algun punto suelto que puede haber quedado
		resultadoString = re.sub("(^|\s)\.($|\s)", "", resultadoString)
		resultadoString = resultadoString.replace("  "," ").strip()

		return resultadoString, resultadoMagnitud, resultadoMetrica, unidadWeb

	def normalizarCantidad(self,cantidad):
		# cantidad tiene un string con el siguiente formato: {magnitud}{metrica} o el string vacio
		magnitud = 1
		metrica = ""
		unidadWeb = cantidad

		if cantidad is not "":
			res = re.findall(r"\d*(?:\.|,|\/)?\d+", cantidad)
			if res:
				numero = max(res, key=len)
				metrica = cantidad.replace(numero,"")

				if metrica == "l":
					metrica = "lt"
				if metrica == "k":
					metrica = "kg"
				if metrica == "g":
					metrica = "gr"

				unidadWeb = numero + metrica

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

		return magnitud, metrica, unidadWeb
	
	def extraerMarca(self,string):
		log = open("log_de_marcas_no_registradas.txt", "a")
		string = string.lower()
		resultadoString = string
		resultadoMarca = ""

		for marca in self.marcas:
			marca = unicode(marca, encoding='utf-8').lower()
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
			log.write("Marca no encontrada: " + resultadoString.encode('utf-8') + '\n')
		return resultadoString, resultadoMarca

	def parsearPrecio(self,precio):
		# Le saco los simbolos de pesos y los espacios
		precio = precio.replace("$U","").replace(" ","")

		# Saco los centesimos
		# Si son mas que 0 le sumo 1 peso al precio
		res = re.findall(r"\.\d\d$", precio)
		if res:
			centesimos = max(res, key=len)
			precio = int(precio.replace(centesimos,""))
			if int(centesimos[1:]) > 0:
				precio += 1
			return precio

		# Obtiene los numeros y ignora cualquier otro caracter
		return int(re.sub("[^0-9]", "", precio))

