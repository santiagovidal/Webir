import json
import elasticsearch
import requests

es = elasticsearch.Elasticsearch()

def setSuper(filename):
	f = open(filename,"r")

	i = 0
	# for linea in f.readlines():
		# print(linea)
	datos = json.loads(f.read())
	# print datos
	for dato in datos:
		print(dato)
		es.index(index='tinglesa', doc_type='productos', body={
			'metrica': dato['metrica'],
			'precio': dato['precio'],
			'marca': dato['marca'],
			'magnitud': dato['magnitud'],
			'packpor': dato['packpor'],
			'nombre': dato['nombre']
		})

def getDatosPorProducto(super,string):
	
    datos = {}
    datos['query'] = {}
    datos['query']['match'] = {}
    datos['query']['match']['nombre'] = {}
    datos['query']['match']['nombre']['query'] = string
    datos['query']['match']['nombre']['operator'] = 'and'
	
	
    respuesta = requests.get('http://localhost:9200/' + super + '/productos/_search', data=json.dumps(datos))
	
    datos_respuesta = json.loads(respuesta.content)
    resultados = datos_respuesta['hits']['hits']
	
    datos_resultado = []
    
    # print resultados
    
	
    for resultado in resultados:
        datos_resultado.append(json.dumps(resultado['_source']))
		
    return (datos_resultado)
		

# print getDatosPorProducto('tinglesa', 'cereales')






