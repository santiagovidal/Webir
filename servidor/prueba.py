import imp
parser = imp.load_source('parser', '../supercrawl/crawlers/moduloParser.py')

p = parser.parser("../supercrawl/crawlers/")
var1, var2, var3 = p.normalizarCantidad("300gr")

print var2