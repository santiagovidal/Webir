# -*- coding: utf-8 -*-
"""
Algoritmo + Sincronización con DB
"""

# TO-DO: Si queda sólo una operación, la clase se borra

import json
# import syncdb # modulo encargado de la sincronizacion con la base de datos

class Busqueda:
    
	def obtenerMejores(self,json_productos,precision):
		# TO-DO: Todavía falta armar el *.json de retorno - por el momento solo imprime por consola
		'''----------------------------------------------------- 
			Asumiendo que json_productos tiene la siguiente forma
			[
				{
				"nombre"   : string, 
				"marca"    : string,     /* "" implica any */
				"magnitud" : int,
				"metrica"  : ml|gr,      /* "" implica que magnitud es una cantidad */
				"packpor"  : int,	/* Asumo que viene 1 por defecto */
				"unidades" : int	 /* Asumo si el cliente no indica esto viene un 1 */
				},
			...
			]
			Notar que no viene el "precio" por razones obvias =P
		---------------------------------------------------------'''
		json_ret = [] # Temporal, aun no devuelve nada, solo imprime resultados
		
		# Leer el *.json
		with open(json_productos) as archivo_datos: 
			datos = json.loads(archivo_datos.read())
		
		# Para cada dato ingresado por el cliente extraer 
		# los productos en un diccionario de cuadruplas
		# que aloja el precio - inicialmente en 0
		lista_quiero = {}
		for dato in datos:
			# Obtener los datos del json
			nombre   = dato["nombre"].lower()
			marca    = dato["marca"] if len(dato["marca"])>0 else None
			metrica  = dato["metrica"].lower()    
			magnitud = dato["magnitud"] 
			packpor  = dato["packpor"] 
			unidades = dato["unidades"]
				  
			# Guardarse una tupla con 
			# < precio=0, packpor_quiero, marca_quiero, id_prod_super, cant_necesito >
			# Siendo
			#   * precio	 : El precio óptimo que me ofrece el super - el mínimo. 
			#		      Default = -1 - No me dieron precio 
			#   * packpor_quiero : El packpor que quiero. 
			#		      Default = packpor - El packpor que yo indico
			#   * marca_quiero   : La marca que quiero. 
			#		      Default = marca - La marca que yo quiero - posiblemente None
			#   * id_prod_super  : El identificador del producto en el super (autonumerado). 
			#		      Default = -1 - Aun no analice ningun producto
			#   * cant_necesito  : La cantidad de productos que yo necesito para satisfacer 
			#		      la magnitud que quiero. 
			#		      Default = unidades
				# (precio,idprod)
			lista_quiero[nombre,magnitud,metrica,marca,packpor,unidades] = (-1,-1)
		
		# TO-DO: Borrar esta línea a continuación - Solo para test
		print("\n********* Yo quiero estos productos... **********\n",lista_quiero)    
		
		# Conectrse a la BD
		# Obtener el resultado en formato *.json
		'''-------------------------------------------------------- 
			El *.json qu eme devuele la BD es del estilo
			[
				{
					"nombre"    : string, 
					"marca"     : string, 
					"metrica"   : gr|ml,
					"magnitud"  : int,
					"packpor"	: int
				},
			 ...
			 ]
		-------------------------------------------------------- '''
			
		
		# COMO PRUEBA ME CARGO EL JSON DE PRUEBA EN BASE AL DE TINGLESA
		# - Después hay que traducir según como se devuelvan los datos de BD
		with open("CorpusTest.json") as archivo_datos:
			datos_super = json.loads(archivo_datos.read())
		
		# TO-DO: Borrar esta línea a continuación - Solo para test
		# print("\n************** En el super hay... ***************\n", datos_super)	
		
		# Para cada dato que me ofrece el super me quedo
		# con aquellos precios de producto que valgan menos
		# segun las especificaciones del usuario
			
		for clave, valor in lista_quiero.items():
			# Obtengo los valores de la lista
			(nombre_quiero,magnitud_quiero,metrica_quiero,marca_quiero,packpor_quiero,unidades_quiero) = clave
			(precio_tengo,idprod_tengo) = valor
			
			# Consulta a la BD
			# ...
			
			for dato_super in datos_super:
				# Obtener los datos del json
				idprod   = dato_super["id"] 
				nombre   = dato_super["nombre"].lower()
				marca    = dato_super["marca"]    # Siempre tiene marca
				metrica  = dato_super["metrica"].lower()
				magnitud = dato_super["magnitud"]   
				packpor  = dato_super["packpor"] 
				precio   = dato_super["precio"]
				
				
				if precision:
					continue
				else:
					if not nombre_quiero in nombre: 
						# caso quiero "leche" -> super tiene "leche descremada" OK
						continue
					
					if marca_quiero != None and not marca_quiero in marca: 
						# caso quiero * -> super tiene "Azucarlito" OK
						print(marca_quiero)
						continue
					
					cant_necesito_packpor = int(packpor_quiero / packpor)
					
					if packpor_quiero % packpor != 0 or cant_necesito_packpor * unidades_quiero < 1: 
						# caso quiero pack x6 -> super tiene pack x3 OK
						continue
										
					# 2  unidad 2 pack 2kg de azucar => 8 unidad 1 pack 1kg de azucar  
					# 12 unidad 1 pack 1lt de coca   => 2 unidad 6 pack 1lt de cocas   
					
					cant_necesito_magnitud = int(magnitud_quiero / magnitud)
					
					if magnitud_quiero % magnitud != 0 or cant_necesito_magnitud * unidades_quiero < 1: 
						# caso quiero 2 unidades de 0.5kg de azucar -> super tiene 1 packpor de 1kg OK
						# caso quiero 1 unidades de 2kg de azucar   -> super tiene 2 packpor de 1kg OK
						continue
					
					if 0 < precio_tengo and precio_tengo < precio * cant_necesito_magnitud * unidades_quiero:
						# caso tengo $X de ese producto -> super ofrece $K*Y, con K*Y <= X OK
						continue
					
					
					lista_quiero[clave] = (precio * cant_necesito_magnitud , idprod)
					
					# caso preciso   : lista_quiero["Azucar",2000,"gr","Azucarlito",1,2] = (36*2*2, 7) <- Si tengo una bolsa de 2kg de azucar
					# caso impreciso : lista_quiero["Azucar",1000,"gr","Azucarlito",1,4] = (36*1*4, 7) <-
			
			
		print("\n************** El algoritmo responde... ***************\n", lista_quiero)	
		
		# # TO-DO: Borrar estas líneas a continuación - Solo para test - Quizas sirva para armar el *.json de retorno 
		# print("\n******* El algoritmo me dice que... *******\n",lista_quiero)
		# for k,v in lista_quiero.items():
			# necesito = v[4]
			# id_prod = v[3]
			# lst_aux_nom_mag_super = [(dato_super["nombre"],dato_super["magnitud"]) for dato_super in datos_super if dato_super["id"] == id_prod]
			# if len(lst_aux_nom_mag_super)==0:
			# print("No se encontro el producto con nombre \""+k[0]+"\"")
			# print("--")
			# continue
			
			# (prod,magnitud) = lst_aux_nom_mag_super[0]
			# metrica = k[1]
			# marca = v[2]
			# magnitud_quiero = k[2]
			# if not marca:
			# print("Necesito ",str(necesito)," de ",prod," (marca cualquiera) a un precio de $",precio, " por unidad/pack (tota: $",str(precio*necesito),") de ",str(magnitud),metrica," para completar ",str(int(necesito/(magnitud_quiero/magnitud)))," de ",str(magnitud_quiero),metrica)
			# else:
			# print("Necesito ",str(necesito)," de ",prod," marca ",marca," a un precio de $",precio, " por unidad/pack (tota: $",str(precio*necesito),") de ",str(magnitud),metrica," para completar ",str(int(necesito/(magnitud_quiero/magnitud)))," de ",str(magnitud_quiero),metrica)
			# print("--")
		
		'''-------------------------------------------------------- 
			El *.json de retorno tendría mas o menos esta forma
			{
			"total" : int,
			"productos":[
				{
				"nombre"   : string, 
				"marca"    : string,     /* "" implica any */
				"magnitud" : int,
				"metrica"  : ml|gr,
				"packpor"  : int	 /* Asumo que viene 1 por defecto */
				"precio"   : int,
				"necesito" : int	 /* cantidad de <magnitud,unidades,packpor> que necesito */
				},
				...
			]
			},
		--------------------------------------------------------''' 
		
		return json_ret	

# TO-DO: Borrar esta línea a continuación - Solo para test
'''-----------------
	Main
--------------------'''
Busqueda().obtenerMejores("EjListaProductosUsuario.json",False)