from flask import Flask, Response, jsonify, render_template, request
import sys
sys.path.append('../UI')
import bdAPI 
import algoritmo
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
        unidadWeb = None if producto["flexible"] else unidadWeb
        packpor = None if producto["desarmable"] else producto["packpor"]
        marca = None if (producto["marca"] == "Cualquiera") else producto["marca"]

        # Tienda Inglesa
        datos = bdAPI.getDatosPorProducto('tinglesa', producto["nombre"], unidadWeb, marca, packpor)
        mejores = algoritmo.Busqueda().obtenerMejores(datos, producto["cantidad"])
        resultado['tinglesa'].append(mejores)

        # Devoto
        datos = bdAPI.getDatosPorProducto('devoto', producto["nombre"], unidadWeb, marca, packpor)
        mejores = algoritmo.Busqueda().obtenerMejores(datos, producto["cantidad"])
        resultado['devoto'].append(mejores)
      
    return json.dumps(resultado)
 


if __name__ == "__main__":
    app.debug = True
    app.run()