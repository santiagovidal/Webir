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
    marca = None if (marca == "cualquiera") else marca
    unidadWeb = request.args.get('unidad', None)
    packpor = request.args.get('packpor', None)
    if prod != None :
        datos = bdAPI.getDatosPorProducto('tinglesa', prod, unidadWeb, marca, packpor)
        datos += bdAPI.getDatosPorProducto('devoto', prod, unidadWeb, marca, packpor)
        return json.dumps(datos)

@app.route("/getMarket", methods=['GET'])
def getMarket():
    prod = request.args.get('prod', None)
    marca = request.args.get('marca', None)
    marca = None if (marca == "cualquiera") else marca
    unidadWeb = request.args.get('unidad', None)
    unidadWeb = None if (unidadWeb == "None") else unidadWeb 
    packpor = request.args.get('packpor', None)
    packpor =None if (packpor == "None") else packpor
    if prod != None :
        datos = bdAPI.getDatosPorProducto('tinglesa', prod, unidadWeb, marca, packpor)
        datos += bdAPI.getDatosPorProducto('devoto', prod, unidadWeb, marca, packpor)
        # ACA SE INVOCA A LA FUNCIÓN QUE CALCULA LA MEJOR TRIPLA PARA ESOS DATOS.
 


if __name__ == "__main__":
    app.debug = True
    app.run()