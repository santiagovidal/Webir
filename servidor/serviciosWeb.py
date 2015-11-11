from flask import Flask, Response, jsonify, render_template, request
import sys
sys.path.append('../UI')
import bdAPI
import json

app = Flask(__name__, template_folder="../UI", static_folder="../UI/static")

@app.route("/")
def index():
    return render_template('index.html',)

###########formato json###########
#{  marca: nomMarca,
#   unidad: magnitud + metrica,   
#   packpor: x + packpor`}
@app.route("/datosPorProducto", methods=['GET'])
def datosPorProducto():
    prod = request.args.get('prod', 0)
    if prod != 0 :
        return json.dumps(bdAPI.getDatosPorProducto('tinglesa', prod))  

 


if __name__ == "__main__":
    app.debug = True
    app.run()