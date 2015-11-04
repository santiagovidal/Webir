from flask import Flask
import bdAPI
import json

app = Flask(__name__)


###########formato json###########
#{  marca: nomMarca,
#   unidad: magnitud + metrica,   
#   packpor: x + packpor`}
@app.route("/datosPorProducto/<producto>")
def datosPorProducto(producto):
    return producto
    # json.dumps(getDatosPorProducto("tinglesa", producto))


    # resultado = {}
    # resultado ["marca"]
    
    

 

if __name__ == "__main__":
    app.run()