import re

class parser (object):
	
	
	def __init__(self):
		f = open("listaMarcas.txt","r")
		self.marcas = f.read().lower().split('\n')

	def extraerCantidad(self, string):
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

	# producto = "Galleta La Sin Rival Granetti Snacks (lt)"
	# tituloSinCantidad, cantidad = extraerCantidad(producto)
	# print("Titulo: " + tituloSinCantidad + "\n")
	# print("Cantidad: " + cantidad + "\n")

	
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

