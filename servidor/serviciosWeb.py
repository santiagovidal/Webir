from flask import Flask, Response, jsonify, render_template, request
import sys
sys.path.append('../supercrawl/crawlers')
import moduloParser 
import bdAPI 
import algoritmo
sys.path.append('../UI')
import json

app = Flask(__name__, template_folder="../UI", static_folder="../UI/static")

@app.route("/")
def index():
    return render_template('index.html',)
	
@app.route("/index.html")
def main():
    return render_template('index.html',)

@app.route("/resultado.html")	
def resultado():
	return render_template('resultado.html',)
	
@app.route("/datosPorProducto", methods=['GET'])
def datosPorProducto():
    prod = request.args.get('prod', None)
    marca = request.args.get('marca', None)
    marca = None if (marca == "Cualquiera") else marca
    unidadWeb = request.args.get('unidad', None)
    unidadWeb = None if (unidadWeb == "Cualquiera") else unidadWeb
    packpor = request.args.get('packpor', None)
    if prod != None :
        datos = bdAPI.getDatosPorProducto('tinglesa', prod, unidadWeb, marca, packpor)
        datos += bdAPI.getDatosPorProducto('devoto', prod, unidadWeb, marca, packpor)
        return json.dumps(datos)

@app.route("/getMarket", methods=['POST'])
def getMarket():
    content = json.loads(request.get_data())
    market = content["market"]
    resultado = {}
    resultado['tinglesa'] = []
    resultado['devoto'] = []

    for producto in market:
        unidadWeb = None if (producto["unidadWeb"]  == "Cualquiera") else producto["unidadWeb"]
        unidadWeb = unidadWeb if producto["magnitudExacta"] else None
        packpor = int(producto["packpor"]) if producto["packExacto"] else None
        marca = None if (producto["marca"] == "Cualquiera") else producto["marca"]
        #quiero_magnitud = moduloParser.parser().normalizarCantidad(unidadWeb)[0] if unidadWeb else None
        
        # Tienda Inglesa
        datos = bdAPI.getDatosPorProducto('tinglesa', producto["nombre"], unidadWeb, marca, packpor)      
        quiero_magnitudquiero_magnitud =  None if unidadWeb else int([dato for dato in datos if dato["unidadWeb"] == unidadWeb][0]["magnitud"])
        quiero_packpor = None if producto["packExacto"] else int(producto["packpor"]) 
        print str(packpor), str(quiero_magnitud)
        mejores = algoritmo.Busqueda().obtenerMejores(datos, producto["cantidad"], quiero_magnitud=quiero_magnitud, quiero_packpor=quiero_packpor)
        resultado['tinglesa'].append(mejores)

        # Devoto
        datos = bdAPI.getDatosPorProducto('devoto', producto["nombre"], unidadWeb, marca, packpor)
        mejores = algoritmo.Busqueda().obtenerMejores(datos, producto["cantidad"], quiero_packpor=packpor, quiero_magnitud=quiero_magnitud)
        resultado['devoto'].append(mejores)
      
    return json.dumps(resultado)
 


if __name__ == "__main__":
    app.debug = True
    app.run()