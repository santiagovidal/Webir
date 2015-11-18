// var id = 2;
var marcas = [];
var unidades = [];
var packs = [];


unique = function(xs) {
  var seen = {}
  return xs.filter(function(x) {
    if (seen[x])
      return
    seen[x] = true
    return x
  })
}

getProduct = function(i){
	// POR AHORA ESTA AGARRANDO SOLO LA INFO QUE SE ESCRIBE
	// ACA FALTARIA HACERSE LA LLAMADA A LA LOGICA PARA TRAER
	// LAS MARCAS Y UNIDAD QUE COINCIDEN CON EL PRODUCTO INGRESADO
    
    $('#selectMarca'+ i).empty();
    marcas = ["cualquiera"];
    $('#selectUnidad'+ i).empty();
    unidades = [];
    $('#selectPack' + i).empty();
    packs = [];
    $("#selectUnidad"+i).attr("disabled",true);
    $("#flexible"+ i).attr("disabled",true);
    $("#selectPack"+i).attr("disabled",true);
    $("#desarmable"+i).attr("disabled",true);
    $("#inputCantidad"+i).attr("disabled",true);
    $("#addButton").attr("disabled",true);
    $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        prod: $('#input' + i).val(),
      }, function(data) {
            for(var j = 0; j < data.length; j++){
                
                var json = JSON.parse(data[j]);
                if (marcas.indexOf(json.marca) == -1 && json.marca.length != 0){
                     marcas.push (json.marca);
                };
            }
            for (var j=0; j < marcas.length; j++){
				var marca = marcas[j];
				marca = marca.toLowerCase().replace( /\b\w/g, function (word) {
					return word.toUpperCase();
				});
				console.log(marca);
                $('#selectMarca' + i).append('<option>'+ marca +'</option>');
            }
            $("#selectMarca"+i).attr("disabled",false);
          
      });    
};

getMarket = function(){
	window.location.href = "resultado.html";
};

startOver = function(){
	window.location.href = "index.html";
};

// $("#selectMarca1").click(function(){
setMarca = function(i){
    $('#selectUnidad'+ (i)).empty();
    unidades = [];
    $('#selectPack' + (i)).empty();
    packs = [];
    $("#selectPack"+(i)).attr("disabled",true);
    $("#desarmable"+(i)).attr("disabled",true);
    $("#inputCantidad"+(i)).attr("disabled",true);
    $("#addButton").attr("disabled",true);
    $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        prod: $('#input' + (i)).val(),
        marca: $('#selectMarca' + (i)).val(),
      }, function(data) {
            for(var j = 0; j < data.length; j++){
                var json = JSON.parse(data[j]);
                if (unidades.indexOf(json.unidadWeb) == -1 && json.unidadWeb.length != 0 && json.marca.length != 0){
                     unidades.push (json.unidadWeb);
                };
            }
            for (var j=0; j < unidades.length; j++){
                $('#selectUnidad' + i).append('<option>'+ unidades[j] +'</option>');
            }
            $("#selectUnidad"+(i)).attr("disabled",false);
            $("#flexible"+(i)).attr("disabled",false);
          
      });    
	
};

setUnidad = function(i){
    $("#inputCantidad"+i).attr("disabled",true);
    $('#selectPack' + i).empty();
    packs = [];
    $("#inputCantidad"+i).attr("disabled",true);
    $("#addButton").attr("disabled",true);
    $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        prod: $('#input' + i).val(),
        marca: $('#selectMarca' + i).val(),
        unidad: $('#selectUnidad' + i).val(),
      }, function(data) {
            for(var j = 0; j < data.length; j++){
                var json = JSON.parse(data[j]);
                if (packs.indexOf('x' + json.packpor) == -1 && json.packpor.length != 0 && json.unidadWeb.length != 0 && json.marca.length != 0){
                     packs.push ('x' + json.packpor);
                };
            }
            for (var j=0; j < packs.length; j++){
                $('#selectPack' + (i)).append('<option>'+ packs[j] +'</option>');
            }
            $("#selectPack"+i).attr("disabled",false);
            $("#desarmable"+i).attr("disabled",false);
          
      });  
	
};

setPack = function(i){
	$("#inputCantidad"+i).attr("disabled",false);
};

setCantidad = function(){
	$("#addButton").attr("disabled",false);
};

addFields = function(i){
	var lastRow = $('#formProductos tbody');
	
	//creo el input de producto
	var input = document.createElement("input");
	input.type = "text";
	input.id = "input"+(i+1);
	input.name = "product";
	input.placeholder = "Ingrese un producto";
	
	//crea la nueva fila
	lastRow.append('<tr><td></td></tr>');
	
	//agrega el input
	$('#formProductos td:last').append(input);
	$('#input'+(i+1)).attr("size","100");
	$('#input'+(i+1)).attr("onchange","getProduct("+ (i+1)+ ")");
	$('#input'+(i+1)).attr("class","product");
	
	//creo los tags html necesarios para el select marca
	var selectMarca = document.createElement("select");
	selectMarca.id = "selectMarca"+(i+1);
	
	//agrega el select marca
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(selectMarca);
	$('#formProductos td:last select').attr('class','form-control');
	$('#formProductos td:last select').attr('disabled',true);
	$('#formProductos td:last select').attr('onClick','setMarca(' +(i+1) +')');

	//agrega los campos a mostrar en el select Marca
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('#formProductos td:last select').append('<option>cualquiera</option>');
	
	//agrega el select unidad
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append('<table><tr></tr></table>');
	
	var selectUnidad = document.createElement("select");
	selectUnidad.id = "selectUnidad"+(i+1);
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos tr:last td').append(selectUnidad);
	$('#selectUnidad'+(i+1)).attr('class','form-control');
	$('#selectUnidad'+(i+1)).attr('disabled',true);
	$('#selectUnidad'+(i+1)).attr('onClick','setUnidad('+ (i+1)+')');
	
	var inputFlexible = document.createElement('input');
	inputFlexible.id = 'flexible'+ (i+1);
	inputFlexible.type = 'checkbox';
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos td:last').append(inputFlexible);
	$('#desarmable'+(i+1)).attr('disabled',true);
	
	//agrega el select pack
	var selectPack = document.createElement("select");
	selectPack.id = "selectPack"+ (i+1);
	
	$('#tbodyProducts').children('tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append('<table><tr></tr></table>');
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos tr:last td').append(selectPack);
	$('#selectPack'+(i+1)).attr('class','form-control');
	$('#selectPack'+(i+1)).attr('disabled',true);
	$('#selectPack'+(i+1)).attr('onClick','setPack('+ (i+1) +')');
	
	var inputDesarmable = document.createElement('input');
	inputDesarmable.id = 'desarmable'+ (i+1);
	inputDesarmable.type = 'checkbox';
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos td:last').append(inputDesarmable);
	$('#desarmable'+(i+1)).attr('disabled',true);	
	
	//agrega el input cantidad
	var inputCantidad = document.createElement("input");
	inputCantidad.type = "text";
	inputCantidad.id = "inputCantidad"+ (i+1);
	inputCantidad.name = "cantidad";
	inputCantidad.placeholder = "Cantidad";
	
	$('#tbodyProducts').children('tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(inputCantidad);
	$('#inputCantidad'+(i+1)).attr("size","5");
	$('#inputCantidad'+(i+1)).attr("onClick","setCantidad()");
	$('#inputCantidad'+(i+1)).attr("class","cantidad");
	$('#inputCantidad'+(i+1)).attr("disabled",true);
	
	// id = id + 1;
    marcas = [];
    packs = [];
    unidades = [];
	$("#addButton").attr("disabled",true);
    $('#addButton').attr("onClick","addFields("+(i+1)+")");
    
};


// $(function() {
    // var getDatos = function(e) {
      // $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        // prod: $('#input' + (id-1)).val(),
      // }, function(data) {
          // dataProd = data;
          
      // });
      // return false;
    // };

    // $('#input' + (id-1)).bind('focusout', getDatos);


    
  // });
// var selectProduct = function(i){
$(function () {
	$(".resultProduct").click(function(){
		//cambio el seleccionado por la clase comun
		var id = "#" + $(this).closest('tr').attr("id");
		$(id).find("td > table").each(function(){
			if ($(this).attr("class") == "resultProductSelected"){
				$(this).attr("class","resultProduct")
			}
		})
		
		//cambio el seleccionado por la clase especial
		$(this).attr("class","resultProductSelected");
		
		//obtengo cantidad y precio unitario
		var quantity = $(this).attr("value");
		var price = $(this).find("tr:last td").text().match(/\d+/g)[0];
		
		//modifico subtotal
		var subtotal = price*quantity;
		var subtotalAnterior = $(id).find("td:last").text().match(/\d+/g)[0];
		$(id).find("td:last").text("$ " + subtotal);
		
		//modifico total
		var supermercado;
		if (id.indexOf("devoto") > -1)
			supermercado = "Devoto";
		else
			supermercado = "Tinglesa";
		var totalActual = $("#table" + supermercado + " tr:last td").text().match(/\d+/g)[0];
		totalActual = parseInt(totalActual) - parseInt(subtotalAnterior) + subtotal;
		$("#table" + supermercado + " tr:last td:last").text("$ " + totalActual);
	});
});