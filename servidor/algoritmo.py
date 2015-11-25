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
        print quiero_cantidad, quiero_magnitud, quiero_packpor
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
                    quiero_cantidad * quiero_magnitud * quiero_packpor / (dato["magnitud"] * dato["packpor"])\
                    if quiero_packpor and quiero_magnitud and\
                    dato["magnitud"] > 0 and dato["packpor"] > 0 and\
                    (quiero_cantidad * quiero_magnitud * quiero_packpor) % (dato["magnitud"] * dato["packpor"]) == 0 else (
                        quiero_cantidad * quiero_packpor / dato["packpor"]\
                        if quiero_packpor and not quiero_magnitud  and\
                        dato["packpor"] > 0 and\
                        (quiero_cantidad * quiero_packpor) % dato["packpor"] == 0 else(
                            quiero_cantidad * quiero_magnitud / dato["magnitud"]\
                            if quiero_magnitud and not quiero_packpor and\
                            dato["magnitud"] > 0 and\
                            (quiero_cantidad * quiero_magnitud) % dato["magnitud"] == 0 else(
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
        
        key = lambda dato: dato["cantidad"]*dato["precio"] if dato["cantidad"] != -1 else 1e10            
        return sorted(datos, key=key)[:3]