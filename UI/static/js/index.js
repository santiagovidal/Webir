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
	console.log("MARCAAA");
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

setPack = function(){
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
	
	//creo los tags html necesarios para el combo marca
	var buttonMarca = document.createElement("button");
	buttonMarca.type="button";
	buttonMarca.id = "dropdownMenuMarca"+id;
	var spanMarca = document.createElement("span");
	var comboMarca = document.createElement("div");
	var ulMarca = document.createElement("ul");
	
	//crea la nueva fila
	lastRow.append('<tr><td></td></tr>');
	
	//agrega el input
	$('#formProductos td:last').append(input);
	$('#input'+id).attr("size","100");
	$('#input'+id).attr("onchange","getProduct()");
	
	//agrega el combo marca
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(comboMarca);
	$('#formProductos td:last div').attr('class','dropdown');
	$('#formProductos td:last div').append(buttonMarca);
	//agrega atributos al button Marca
	$('#dropdownMenuMarca'+id).html("Marca ");
	$('#dropdownMenuMarca'+id).attr("class","btn btn-default dropdown-toggle");
	$('#dropdownMenuMarca'+id).attr("data-toggle", "dropdown");
	$('#dropdownMenuMarca'+id).attr("aria-haspopup", "true");
	$('#dropdownMenuMarca'+id).attr("aria-expanded", "true");
	$('#dropdownMenuMarca'+id).append(spanMarca);
	$('#dropdownMenuMarca'+id+' span').attr("class","caret");
	$('#formProductos td:last div').append(buttonMarca);
	//agrega el dropdown que va a mostrar
	$('#formProductos td:last div').append(ulMarca);
	$('#formProductos td:last div ul').attr("class","dropdown-menu");
	$('#formProductos td:last div ul').attr("aria-labelledby","dropdownMenu"+id);
	//agrega los campos a mostrar en el button Marca
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('#formProductos td:last div ul').append('<li></li>');
	$('#formProductos td:last div li').append('<a href="#">Marca 1</a>');
	$('#formProductos td:last div li').append('<a href="#">Marca 2</a>');
	$('#formProductos td:last div li').append('<a href="#">Marca 3</a>');
	$('#formProductos td:last div li').append('<a href="#">Marca 4</a>');
	
	//agrega el input magnitud
	var inputMagnitud = document.createElement("input");
	inputMagnitud.type = "text";
	inputMagnitud.id = "magnitud"+id;
	inputMagnitud.size = "20";
	inputMagnitud.placeholder = "Ingrese magnitud";
	
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(inputMagnitud);
	$('#formProductos td:last input').attr('class','magnitud');
	
	//agrega el combo cantidad
	var buttonCantidad = document.createElement("button");
	buttonCantidad.type="button";
	buttonCantidad.id = "dropdownMenuCantidad"+id;
	var spanCantidad = document.createElement("span");
	var comboCantidad = document.createElement("div");
	var ulCantidad = document.createElement("ul");
	
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(comboCantidad);
	$('#formProductos td:last div').attr('class','dropdown');
	$('#formProductos td:last div').append(buttonCantidad);
	//agrega atributos al button Cantidad
	$('#dropdownMenuCantidad'+id).html("Cantidad ");
	$('#dropdownMenuCantidad'+id).attr("class","btn btn-default dropdown-toggle");
	$('#dropdownMenuCantidad'+id).attr("data-toggle", "dropdown");
	$('#dropdownMenuCantidad'+id).attr("aria-haspopup", "true");
	$('#dropdownMenuCantidad'+id).attr("aria-expanded", "true");
	$('#dropdownMenuCantidad'+id).append(spanCantidad);
	$('#dropdownMenuCantidad'+id+' span').attr("class","caret");
	$('#formProductos td:last div').append(buttonCantidad);
	//agrega el dropdown que va a mostrar
	$('#formProductos td:last div').append(ulCantidad);
	$('#formProductos td:last div ul').attr("class","dropdown-menu");
	$('#formProductos td:last div ul').attr("aria-labelledby","dropdownMenu"+id);
	//agrega los campos a mostrar en el button Cantidad
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('#formProductos td:last div ul').append('<li></li>');
	$('#formProductos td:last div li').append('<a href="#">1</a>');
	$('#formProductos td:last div li').append('<a href="#">2</a>');
	$('#formProductos td:last div li').append('<a href="#">3</a>');
	$('#formProductos td:last div li').append('<a href="#">4</a>');
	
	//agrega el combo unidad
	var buttonUnidad = document.createElement("button");
	buttonUnidad.type="button";
	buttonUnidad.id = "dropdownMenuUnidad"+id;
	var spanUnidad = document.createElement("span");
	var comboUnidad = document.createElement("div");
	var ulUnidad = document.createElement("ul");
	
	$('#formProductos tr:last').append('<td class="td-center"></td>');
	$('#formProductos td:last').append(comboUnidad);
	$('#formProductos td:last div').attr('class','dropdown');
	$('#formProductos td:last div').append(buttonUnidad);
	//agrega atributos al button Unidad
	$('#dropdownMenuUnidad'+id).html("Unidad ");
	$('#dropdownMenuUnidad'+id).attr("class","btn btn-default dropdown-toggle");
	$('#dropdownMenuUnidad'+id).attr("data-toggle", "dropdown");
	$('#dropdownMenuUnidad'+id).attr("aria-haspopup", "true");
	$('#dropdownMenuUnidad'+id).attr("aria-expanded", "true");
	$('#dropdownMenuUnidad'+id).append(spanUnidad);
	$('#dropdownMenuUnidad'+id+' span').attr("class","caret");
	$('#formProductos td:last div').append(buttonUnidad);
	//agrega el dropdown que va a mostrar
	$('#formProductos td:last div').append(ulUnidad);
	$('#formProductos td:last div ul').attr("class","dropdown-menu");
	$('#formProductos td:last div ul').attr("aria-labelledby","dropdownMenu"+id);
	//agrega los campos a mostrar en el button Unidad
	//esto capaz se puede ir si van a cargarse a demanda segun el producto
	$('#formProductos td:last div ul').append('<li></li>');
	$('#formProductos td:last div li').append('<a href="#">Litros</a>');
	$('#formProductos td:last div li').append('<a href="#">Mililitros</a>');
	$('#formProductos td:last div li').append('<a href="#">Kilos</a>');
	$('#formProductos td:last div li').append('<a href="#">Gramos</a>');
	
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
