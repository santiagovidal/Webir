import json
import requests

def setSuper(nombreSuper):
    if nombreSuper == "devoto":
        filename = "../supercrawl/crawlers/productosDevotoParseados.json"
    else:
        filename = "../supercrawl/crawlers/productosTInglesaParseados.json"
    f = open(filename,"r")

    datos = json.loads(f.read())
    # print datos
    for dato in datos:
        print(dato)
        respuesta = requests.post('http://localhost:9200/' + nombreSuper + '/productos', data=json.dumps(dato))

def getDatosPorProducto(nombreSuper,nombreProducto, unidadWeb=None, marca=None, packpor=None):
    # Retorna 
    # [
    #     "{
    #         \"metrica\": \"ml\", 
    #         \"precio\": 263, 
    #         \"marca\": \"stella artois\", 
    #         \"packpor\": 3, 
    #         \"unidadWeb\": \"0.975lt\", 
    #         \"nombre\": \"cerveza pack\", 
    #         \"magnitud\": 975
    #     }"
    # ]

    listaQuery = []

    campo = {}
    campo['match'] = {}
    campo['match']['nombre'] = {}
    campo['match']['nombre']['query'] = nombreProducto
    campo['match']['nombre']['operator'] = 'and'
    listaQuery.append(campo)

    if marca:
        campo = {}
        campo['match_phrase'] = {}
        campo['match_phrase']['marca'] = marca
        listaQuery.append(campo)

    if unidadWeb:
        campo = {}
        campo['match'] = {}
        campo['match']['unidadWeb'] = unidadWeb
        listaQuery.append(campo)

    if packpor:
        campo = {}
        campo['match'] = {}
        campo['match']['packpor'] = packpor
        listaQuery.append(campo)

    datos = {}
    datos['from'] = 0
    datos['size'] = 10000
    datos['query'] = {}
    datos['query']['bool'] = {}
    datos['query']['bool']['must'] = listaQuery

    respuesta = requests.get('http://localhost:9200/' + nombreSuper + '/productos/_search', data=json.dumps(datos))
        
    datos_respuesta = json.loads(respuesta.content)
    
    resultados = []
    if datos_respuesta['hits']:
        resultados = datos_respuesta['hits']['hits']
    
    datos_resultado = []
    
    
    for resultado in resultados:
        datos_resultado.append(json.dumps(resultado['_source']))
        
    return (datos_resultado)


# setSuper("tinglesa")
# setSuper("devoto")


