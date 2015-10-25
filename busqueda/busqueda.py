# -*- coding: utf-8 -*-
"""
Algoritmo + Sincronización con DB
"""

# TO-DO: Si queda sólo una operación, la clase se borra

import json
# import syncdb # modulo encargado de la sincronizacion con la base de datos

class Busqueda:
    
    def obtenerMejores(self,json_productos):
        # TO-DO: Todavía falta armar el *.json de retorno - por el momento solo imprime por consola
        '''----------------------------------------------------- 
        Asumiendo que json_productos tiene la siguiente forma
        [
            {
                "nombre"   : string, 
                "marca"    : string,     /* "" implica any */
                "magnitud" : int,
                "unidad"   : ml|gr,      /* "" implica que magnitud es una cantidad */
                "packpor"  : int         /* Asumo que viene 1 por defecto */
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
            unidad   = dato["unidad"].lower()    
            magnitud = dato["magnitud"] 
            packpor  = dato["packpor"] 
                      
            # Guardarse una tupla con 
            # < precio=0, packpor_quiero, marca_quiero, id_prod_super, cant_necesito >
            # Siendo
            #   * precio         : El precio óptimo que me ofrece el super - el mínimo. 
            #                      Default = -1 - No me dieron precio 
            #   * packpor_quiero : El packpor que quiero. 
            #                      Default = packpor - El packpor que yo indico
            #   * marca_quiero   : La marca que quiero. 
            #                      Default = marca - La marca que yo quiero - posiblemente None
            #   * id_prod_super  : El identificador del producto en el super (autonumerado). 
            #                      Default = -1 - Aun no analice ningun producto
            #   * cant_necesito  : La cantidad de productos que yo necesito para satisfacer 
            #                      la magnitud que quiero. 
            #                      Default = 1 - Al menos necesito una unidad de producto
            lista_quiero[nombre,unidad,magnitud] = [-1,packpor,marca,-1,1]
        
        # TO-DO: Borrar esta línea a continuación - Solo para test
        print("\n********* Yo quiero estos productos... **********\n",lista_quiero)    
        
        # Conectrse a la BD
        # Obtener el resultado en formato *.json
        
        # COMO PRUEBA ME CARGO EL JSON DE PRUEBA EN BASE AL DE TINGLESA
        # - Después hay que traducir según como se devuelvan los datos de BD
        with open("CorpusTest.json") as archivo_datos: 
            datos_super = json.loads(archivo_datos.read())
        
        # TO-DO: Borrar esta línea a continuación - Solo para test
        # print("\n************** En el super hay... ***************\n", datos_super)        
        
        # Para cada dato que me ofrece el super me quedo
        # con aquellos precios de producto que valgan menos
        # segun las especificaciones del usuario
        for dato_super in datos_super:
            # Obtener los datos del json
            id_prod  = dato_super["id"] 
            nombre   = dato_super["nombre"].lower()
            marca    = dato_super["marca"]    # Siempre tiene marca
            unidad   = dato_super["unidad"].lower()
            magnitud = dato_super["magnitud"]   
            packpor  = dato_super["packpor"] 
            precio   = dato_super["precio"]
            
            # Obtengo una lista de tuplas < nombre_producto, cantidad_necesito >           
            # tal que:
            #   * nombre_producto - Es el nombre de producto que yo quiero y
            #     además sea un substring del producto que estoy mirando 
            #     actualmente y cuya unidad sea la que yo quiero
            #   * cantidad_necesito - Es la cantidad que necesito de ese producto
            #     para cumplir con mis necesidades
            filtro = [(nombre_prod_substr, int(magnitud_quiero / magnitud))           # dame aquellos nombres de producto  
                 for (nombre_prod_substr,unidad,magnitud_quiero) in lista_quiero      # tal que ese nombres lo tengo en mi lista de productos                 
                 if nombre_prod_substr in nombre and magnitud_quiero % magnitud == 0] # y ademas es substring del nombre del producto que estoy analizando

            # OJO: Esto puede dar problemas si en mi lista tengo p.e. "Agua Sirte" y "Agua Salus"
            nombre_producto  = filtro[0][0] if len(filtro) == 1 else None
            cant_necesito    = filtro[0][1] if len(filtro) == 1 else None
            
            if not nombre_producto: # Si no matcheo la búsqueda, buscá otro
                continue
            
            # Cambiar el precio optimo de la tupla del diccionario si...
            # 1 - el producto esta en mi lista
            # 2 - el packpor que me ofrecen es menor al que yo quiero 
            # 3 - la marca es es la que me ofrecen o es None si quiero todas
            # 4 - el precio*pack que me ofrecen es menor al que tengo hasta el momento
            magnitud_necesito = magnitud*cant_necesito            
            
            if (packpor <= lista_quiero[nombre_producto,unidad,magnitud_necesito][1]
              and (
                  marca == lista_quiero[nombre_producto,unidad,magnitud_necesito][2] 
                  or 
                  not lista_quiero[nombre_producto,unidad,magnitud_necesito][2]
              )
              and (
                  precio*packpor*cant_necesito < lista_quiero[nombre_producto,unidad,magnitud_necesito][0]
                  or
                  # Esto es medio chancho, pero Python no tiene un maxint
                  lista_quiero[nombre_producto,unidad,magnitud_necesito][0] == -1 
              )):                    
                lista_quiero[nombre_producto,unidad,magnitud_necesito][0] = precio*packpor*cant_necesito
                lista_quiero[nombre_producto,unidad,magnitud_necesito][3] = id_prod
                lista_quiero[nombre_producto,unidad,magnitud_necesito][4] = cant_necesito
        
        # TO-DO: Borrar estas líneas a continuación - Solo para test - Quizas sirva para armar el *.json de retorno 
        print("\n******* El algoritmo me dice que... *******")
        for k,v in lista_quiero.items():
            necesito = v[4]
            id_prod = v[3]
            lst_aux_nom_mag_super = [(dato_super["nombre"],dato_super["magnitud"]) for dato_super in datos_super if dato_super["id"] == id_prod]
            if len(lst_aux_nom_mag_super)==0:
                print("No se encontro el producto con nombre \""+k[0]+"\"")
                print("--")
                continue
            
            (prod,magnitud) = lst_aux_nom_mag_super[0]
            unidad = k[1]
            marca = v[2]
            magnitud_quiero = k[2]
            if not marca:
                print("Necesito ",str(necesito)," de ",prod," (marca cualquiera) a un precio de ",precio, " por unidad/pack de ",str(magnitud),unidad," para completar ",str(magnitud_quiero),unidad)
            else:
                print("Necesito ",str(necesito)," de ",prod," marca ",marca," a un precio de ",precio, " por unidad/pack de ",str(magnitud),unidad," para completar ",str(magnitud_quiero),unidad)
            print("--")
        
        '''-------------------------------------------------------- 
            El *.json de retorno tendría mas o menos esta forma
            {
                "total" : int,
                "productos":[
                    {
                        "nombre"   :string, 
                        "marca"    :string,     /* "" implica any */
                        "magnitud" :int,
                        "unidad"   :ml|gr,
                        "packpor"  : int         /* Asumo que viene 1 por defecto */
                        "precio"   :int,
                        "necesito" :int         /* cantidad de <magnitud,unidades,packpor> que necesito */
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
Busqueda().obtenerMejores("EjListaProductosUsuario.json")