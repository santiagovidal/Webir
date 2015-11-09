# Este script sirve para ordenar la lista de marcas de forma descenciente
# Usando el largo del nombre como criterio
# Esto sirve para darle prioridad a la marca de nombre mas largo
# En caso de que un producto matchee varias marcas
# Ya que el parser se queda con la primera marca que encuentra

f1 = open("listaMarcas.txt","r")
marcas = f1.read().split('\n')

marcas.sort(key = len, reverse=True)

f2 = open("listaMarcasNueva.txt","w")
for marca in marcas:
	f2.write(marca + '\n')

f1.close()
f2.close()