var id = 2;
var dataProd;

getProduct = function(){
	// POR AHORA ESTA AGARRANDO SOLO LA INFO QUE SE ESCRIBE
	// ACA FALTARIA HACERSE LA LLAMADA A LA LOGICA PARA TRAER
	// LAS MARCAS Y UNIDAD QUE COINCIDEN CON EL PRODUCTO INGRESADO
	
	var idProduct = $("#input"+(id-1)).val();
	console.log(idProduct);
	$("#selectMarca"+(id-1)).attr("disabled",false);
};

getMarket = function(){
	window.location.href = "resultado.html";
};

// $("#selectMarca1").click(function(){
setMarca = function(){
	$("#selectUnidad"+(id-1)).attr("disabled",false);
	$("#flexible"+(id-1)).attr("disabled",false);
};

setUnidad = function(){
	$("#selectPack"+(id-1)).attr("disabled",false);
	$("#desarmable"+(id-1)).attr("disabled",false);
};

setPack = function(){
	$("#inputCantidad"+(id-1)).attr("disabled",false);
};

setCantidad = function(){
	$("#addButton").attr("disabled",false);
};

addFields = function(){
	var lastRow = $('#formProductos tbody');
	
	//creo el input de producto
	var input = document.createElement("input");
	input.type = "text";
	input.id = "input"+id;
	input.name = "product";
	input.placeholder = "Ingrese un producto";
	
	//crea la nueva fila
	lastRow.append('<tr><td></td></tr>');
	
	//agrega el input
	$('#formProductos td:last').append(input);
	$('#input'+id).attr("size","100");
	$('#input'+id).attr("onchange","getProduct()");
	$('#input'+id).attr("class","product");
	
	//creo los tags html necesarios para el select marca
	var selectMarca = document.createElement("select");
	selectMarca.id = "selectMarca"+id;
	
	//agrega el select marca
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(selectMarca);
	$('#formProductos td:last select').attr('class','form-control');
	$('#formProductos td:last select').attr('disabled',true);
	$('#formProductos td:last select').attr('onClick','setMarca()');

	//agrega los campos a mostrar en el select Marca
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('#formProductos td:last select').append('<option>Marca 1</option>');
	$('#formProductos td:last select').append('<option>Marca 2</option>');
	$('#formProductos td:last select').append('<option>Marca 3</option>');
	
	//agrega el select unidad
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append('<table><tr></tr></table>');
	
	var selectUnidad = document.createElement("select");
	selectUnidad.id = "selectUnidad"+id;
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos tr:last td').append(selectUnidad);
	$('#selectUnidad'+id).attr('class','form-control');
	$('#selectUnidad'+id).attr('disabled',true);
	$('#selectUnidad'+id).attr('onClick','setUnidad()');
	
	//agrega los campos a mostrar en el button Marca
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('#selectUnidad'+id).append('<option>Unidad 1</option>');
	$('#selectUnidad'+id).append('<option>Unidad 2</option>');
	$('#selectUnidad'+id).append('<option>Unidad 3</option>');
	
	var inputFlexible = document.createElement('input');
	inputFlexible.id = 'flexible'+id;
	inputFlexible.type = 'checkbox';
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos td:last').append(inputFlexible);
	$('#desarmable'+id).attr('disabled',true);
	
	//agrega el select pack
	var selectPack = document.createElement("select");
	selectPack.id = "selectPack"+id;
	
	$('#tbodyProducts').children('tr:last').append('<td class="td-center"></td>');
	$('#formProductos tr:last-child td:last').append(selectPack);
	$('selectPack'+id).attr('class','form-control');
	$('selectPack'+id).attr('disabled',true);
	$('selectPack'+id).attr('onClick','setPack()');
	
	//agrega los campos a mostrar en el select pack
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('selectPack'+id).append('<option>x6</option>');
	$('selectPack'+id).append('<option>x12</option>');	
	
	//agrega el input cantidad
	var inputCantidad = document.createElement("input");
	inputCantidad.type = "text";
	inputCantidad.id = "inputCantidad"+id;
	inputCantidad.name = "cantidad";
	inputCantidad.placeholder = "Cantidad";
	
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(inputCantidad);
	$('#inputCantidad'+id).attr("size","5");
	$('#input'+id).attr("onchange","getProduct()");
	$('#input'+id).attr("class","cantidad");
	$('#input'+id).attr("disabled",true);
	
	id = id + 1;
	$("#addButton").attr("disabled",true);
};


$(function() {
    var getDatos = function(e) {
      $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        a: $('input' + (id-1)).val(),
      }, function(data) {
          dataProd = data;
          alert (dataProd);
      });
      return false;
    };

    $('#prueba').bind('click', getDatos);

    
  });
