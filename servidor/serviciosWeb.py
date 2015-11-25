from flask import Flask, Response, jsonify, render_template, request
import sys
import imp
parser = imp.load_source('parser', '../supercrawl/crawlers/moduloParser.py')
p = parser.parser("../supercrawl/crawlers/") 
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
        quiero_magnitud = None if (producto["unidadWeb"]  == "Cualquiera") else p.normalizarCantidad(producto["unidadWeb"])[0]                
        quiero_magnitud = None if producto["magnitudExacta"] else quiero_magnitud 
        
        packpor = int(producto["packpor"]) if producto["packExacto"] else None
        quiero_packpor = None if producto["packExacto"] else int(producto["packpor"]) 
        
        marca = None if (producto["marca"] == "Cualquiera") else producto["marca"]
        
        
        # Tienda Inglesa
        datos = bdAPI.getDatosPorProducto('tinglesa', producto["nombre"], unidadWeb, marca, packpor)      
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