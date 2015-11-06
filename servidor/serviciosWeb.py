from flask import Flask
from flask import jsonify
import bdAPI
import json

app = Flask(__name__)


###########formato json###########
#{  marca: nomMarca,
#   unidad: magnitud + metrica,   
#   packpor: x + packpor`}
@app.route("/datosPorProducto/<producto>")
def datosPorProducto(producto):
    return json.dumps(bdAPI.getDatosPorProducto("tinglesa", producto))
 
    

 

if __name__ == "__main__":
    # app.debug = True
    app.run()