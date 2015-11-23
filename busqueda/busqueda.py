# -*- coding: utf-8 -*-
"""
Algoritmo + Sincronización con DB
"""

# TO-DO: Si queda sólo una operación, la clase se borra

import json

class Busqueda:
    
	def obtenerMejores(self,
		datos,
		quiero_cantidad,
		quiero_magnitud = None,
		quiero_packpor = None
	):
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
		datos = [
			dict(
			 	dato.items() +\
			 	[(
					u'cantidad',
					quiero_cantidad * (quiero_magnitud / dato["magnitud"]) * (quiero_packpor / dato["packpor"])\
					if quiero_packpor and quiero_magnitud and\
					dato["magnitud"] > 0 and dato["packpor"] > 0 and\
					quiero_magnitud % dato["magnitud"] == 0 and\
					quiero_packpor % dato["packpor"] == 0 else (
						quiero_cantidad * (quiero_packpor / dato["packpor"])\
						if quiero_packpor and not quiero_magnitud  and\
						dato["packpor"] > 0 and\
						quiero_packpor % dato["packpor"] == 0 else(
							quiero_cantidad * (quiero_magnitud / dato["magnitud"])\
							if quiero_magnitud and not quiero_packpor and\
							dato["magnitud"] > 0 and\
							quiero_magnitud % dato["magnitud"] == 0 else(
								 quiero_cantidad\
								 if not (quiero_magnitud or quiero_packpor) else(
									-1
								)
							)
						)  
					) 
				)]
			) for dato in datos
        ]

		if not (quiero_magnitud or quiero_packpor):
			key = lambda dato: dato["cantidad"]*dato["precio"]
		elif quiero_magnitud and not quiero_packpor:
		 	key = lambda dato: dato["cantidad"]*dato["precio"]*(quiero_magnitud/dato["magnitud"])\
					if dato["magnitud"] > 0 and\
					quiero_magnitud % dato["magnitud"] == 0  else 1e10
		elif not quiero_magnitud and quiero_packpor:
			 key = lambda dato: dato["cantidad"]*dato["precio"]*(quiero_packpor/dato["packpor"])\
					if dato["packpor"] > 0 and\
					quiero_packpor % dato["packpor"] == 0 else 1e10
		else:
			key = lambda dato: dato["cantidad"]*dato["precio"]*(quiero_packpor/dato["packpor"])*(quiero_magnitud/dato["magnitud"])\
					if dato["packpor"] > 0 and dato["magnitud"] > 0 and\
					quiero_packpor % dato["packpor"] == 0 and\
					quiero_magnitud % dato["magnitud"] == 0 else 1e10
			
		return sorted(datos, key=key)[:3]