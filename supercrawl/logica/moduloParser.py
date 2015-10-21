import re

class parser (object):
	
	
	def __init__(self):
		f = open("listaMarcas.txt","r")
		self.marcas = f.read().lower().split('\n')

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

		# Multiplicadores - lo agrego a lo que tengo antes con un espacio entre medio
		res = re.findall(r"x\d+u?", resultadoString)
		if res:
			resultadoString = resultadoString.replace(max(res, key=len),"").replace("  "," ").strip()
			if resultadoCantidad != "":
				resultadoCantidad += " "
			resultadoCantidad += max(res, key=len)

		if resultadoCantidad == "":
			log.write("Cantidad no encontrada: " + resultadoString + '\n')
		return resultadoString, resultadoCantidad

	def normalizarCantidad(cantidad):
		# Primero pasar lt a ml o kg a gr
		cantidadNormalizada = cantidad

		if "lt" in cantidad or "kg" in cantidad:
			res = re.findall(r"\d*(?:\.|,|\/)?\d+", cantidad)
			if res:
				numero = max(res, key=len)
				numeroNormalizado = str(int(float(numero.replace(",","."))*1000))
				cantidadNormalizada = cantidadNormalizada.replace(numero,numeroNormalizado)
				cantidadNormalizada = cantidadNormalizada.replace("kg","gr")
				cantidadNormalizada = cantidadNormalizada.replace("lt","ml")


		return cantidadNormalizada

	cant = "1.31123lt"
	cantNormalizada = normalizarCantidad(cant)
	print("Cantidad: " + cantNormalizada + "\n")

	
	def extraerMarca(self,string):
		log = open("log_de_marcas_no_registradas.txt", "a")
		string = string.lower()
		resultadoString = string
		resultadoMarca = ""
		for marca in self.marcas:
			# marca = marca.lower().replace('\n','')
			
			if re.compile('\s'+marca+'(\s|$)').search(string) is not None:
				resultadoString = re.sub("\s"+marca,"",string) 
				resultadoMarca = marca
				break
				
		if resultadoMarca == "":
			log.write("Marca no encontrada: " + resultadoString + '\n')
		return resultadoString, resultadoMarca

	# producto = "Galleta La Sin Rival Granetti Snacks 200gr"
	# tituloSinMarca, marca = extraerMarca(producto,marcas)
	# print("Titulo: " + tituloSinMarca + "\n")
	# print("Marca: " + marca + "\n")

