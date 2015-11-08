from flask import Flask
from flask import render_template
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
@app.route("/datosPorProducto/<producto>", methods=['GET'])
def datosPorProducto(producto):
    return json.dumps(bdAPI.getDatosPorProducto("tinglesa", producto))
 
    

 

if __name__ == "__main__":
    app.debug = True
    app.run()