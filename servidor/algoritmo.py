# -*- coding: utf-8 -*-
"""
Algoritmo + Sincronizaci�n con DB
"""

# TO-DO: Si queda s�lo una operaci�n, la clase se borra

import json
# import syncdb # modulo encargado de la sincronizacion con la base de datos

class Busqueda:
    
	def obtenerMejores(self,
		datos,
		quiero_cantidad,
		quiero_metrica = None,
		quiero_packpor = None
	):
		# TO-DO: Todav�a falta armar el *.json de retorno - por el momento solo imprime por consola
		'''----------------------------------------------------- 
			Asumiendo que json_productos tiene la siguiente forma
			[
				{
					"metrica": gr|ml, 
					"precio": int, 
					"marca": string, 
					"packpor": int, 
					"unidadWeb": string, 
					"nombre": string, 
					"magnitud": int
				},
			...
			]
		---------------------------------------------------------'''

		# Incluyo la cantidad a cada dato de la BD
		datos = [dict(dato.items() + [(u'cantidad',quiero_cantidad)]) for dato in datos]

		# Si prefiero los datos precisos
		if not (quiero_metrica or quiero_packpor):
			key = lambda dato: dato["precio"]
		# else:
		# 	key = lambda dato: [
		# 		dato
		# 		dato["cantidad"]*dato["precio"]/dato["packpor"],

		# 	]
		
		return sorted(datos, key=key)[:3]

		# # TO-DO: Borrar esta l�nea a continuaci�n - Solo para test
		# print("\n********* Yo quiero estos productos... **********\n",lista_quiero)    
		
		# # Conectrse a la BD
		# # Obtener el resultado en formato *.json
		# '''-------------------------------------------------------- 
		# 	El *.json qu eme devuele la BD es del estilo
		# 	[
		# 		{
		# 			"nombre"    : string, 
		# 			"marca"     : string, 
		# 			"metrica"   : gr|ml,
		# 			"magnitud"  : int,
		# 			"packpor"	: int
		# 		},
		# 	 ...
		# 	 ]
		# -------------------------------------------------------- '''
			
		
		# # COMO PRUEBA ME CARGO EL JSON DE PRUEBA EN BASE AL DE TINGLESA
		# # - Despu�s hay que traducir seg�n como se devuelvan los datos de BD
		# with open("CorpusTest.json") as archivo_datos:
		# 	datos_super = json.loads(archivo_datos.read())
		
		# # TO-DO: Borrar esta l�nea a continuaci�n - Solo para test
		# # print("\n************** En el super hay... ***************\n", datos_super)	
		
		# # Para cada dato que me ofrece el super me quedo
		# # con aquellos precios de producto que valgan menos
		# # segun las especificaciones del usuario
			
		# for clave, valor in lista_quiero.items():
		# 	# Obtengo los valores de la lista
		# 	(nombre_quiero,magnitud_quiero,metrica_quiero,marca_quiero,packpor_quiero,unidades_quiero) = clave
		# 	(precio_tengo,idprod_tengo) = valor
			
		# 	# Consulta a la BD
		# 	# ...
			
		# 	for dato_super in datos_super:
		# 		# Obtener los datos del json
		# 		idprod   = dato_super["id"] 
		# 		nombre   = dato_super["nombre"].lower()
		# 		marca    = dato_super["marca"]    # Siempre tiene marca
		# 		metrica  = dato_super["metrica"].lower()
		# 		magnitud = dato_super["magnitud"]   
		# 		packpor  = dato_super["packpor"] 
		# 		precio   = dato_super["precio"]
				
				
		# 		if precision:
		# 			continue
		# 		else:
		# 			if not nombre_quiero in nombre: 
		# 				# caso quiero "leche" -> super tiene "leche descremada" OK
		# 				continue
					
		# 			if marca_quiero != None and not marca_quiero in marca: 
		# 				# caso quiero * -> super tiene "Azucarlito" OK
		# 				print(marca_quiero)
		# 				continue
					
		# 			cant_necesito_packpor = int(packpor_quiero / packpor)
					
		# 			if packpor_quiero % packpor != 0 or cant_necesito_packpor * unidades_quiero < 1: 
		# 				# caso quiero pack x6 -> super tiene pack x3 OK
		# 				continue
										
		# 			# 2  unidad 2 pack 2kg de azucar => 8 unidad 1 pack 1kg de azucar  
		# 			# 12 unidad 1 pack 1lt de coca   => 2 unidad 6 pack 1lt de cocas   
					
		# 			cant_necesito_magnitud = int(magnitud_quiero / magnitud)
					
		# 			if magnitud_quiero % magnitud != 0 or cant_necesito_magnitud * unidades_quiero < 1: 
		# 				# caso quiero 2 unidades de 0.5kg de azucar -> super tiene 1 packpor de 1kg OK
		# 				# caso quiero 1 unidades de 2kg de azucar   -> super tiene 2 packpor de 1kg OK
		# 				continue
					
		# 			if 0 < precio_tengo and precio_tengo < precio * cant_necesito_magnitud * unidades_quiero:
		# 				# caso tengo $X de ese producto -> super ofrece $K*Y, con K*Y <= X OK
		# 				continue
					
					
		# 			lista_quiero[clave] = (precio * cant_necesito_magnitud , idprod)
					
		# 			# caso preciso   : lista_quiero["Azucar",2000,"gr","Azucarlito",1,2] = (36*2*2, 7) <- Si tengo una bolsa de 2kg de azucar
		# 			# caso impreciso : lista_quiero["Azucar",1000,"gr","Azucarlito",1,4] = (36*1*4, 7) <-
			
			
		# print("\n************** El algoritmo responde... ***************\n", lista_quiero)	
		
		# # # TO-DO: Borrar estas l�neas a continuaci�n - Solo para test - Quizas sirva para armar el *.json de retorno 
		# # print("\n******* El algoritmo me dice que... *******\n",lista_quiero)
		# # for k,v in lista_quiero.items():
		# 	# necesito = v[4]
		# 	# id_prod = v[3]
		# 	# lst_aux_nom_mag_super = [(dato_super["nombre"],dato_super["magnitud"]) for dato_super in datos_super if dato_super["id"] == id_prod]
		# 	# if len(lst_aux_nom_mag_super)==0:
		# 	# print("No se encontro el producto con nombre \""+k[0]+"\"")
		# 	# print("--")
		# 	# continue
			
		# 	# (prod,magnitud) = lst_aux_nom_mag_super[0]
		# 	# metrica = k[1]
		# 	# marca = v[2]
		# 	# magnitud_quiero = k[2]
		# 	# if not marca:
		# 	# print("Necesito ",str(necesito)," de ",prod," (marca cualquiera) a un precio de $",precio, " por unidad/pack (tota: $",str(precio*necesito),") de ",str(magnitud),metrica," para completar ",str(int(necesito/(magnitud_quiero/magnitud)))," de ",str(magnitud_quiero),metrica)
		# 	# else:
		# 	# print("Necesito ",str(necesito)," de ",prod," marca ",marca," a un precio de $",precio, " por unidad/pack (tota: $",str(precio*necesito),") de ",str(magnitud),metrica," para completar ",str(int(necesito/(magnitud_quiero/magnitud)))," de ",str(magnitud_quiero),metrica)
		# 	# print("--")
		
		# '''-------------------------------------------------------- 
		# 	El *.json de retorno tendr�a mas o menos esta forma
		# 	{
		# 	"total" : int,
		# 	"productos":[
		# 		{
		# 		"nombre"   : string, 
		# 		"marca"    : string,     /* "" implica any */
		# 		"magnitud" : int,
		# 		"metrica"  : ml|gr,
		# 		"packpor"  : int	 /* Asumo que viene 1 por defecto */
		# 		"precio"   : int,
		# 		"necesito" : int	 /* cantidad de <magnitud,unidades,packpor> que necesito */
		# 		},
		# 		...
		# 	]
		# 	},
		# --------------------------------------------------------''' 
		
		# return json_ret	

# TO-DO: Borrar esta l�nea a continuaci�n - Solo para test
'''-----------------
	Main
--------------------'''
#Busqueda().obtenerMejores("EjListaProductosUsuario.json",False)