var cantCampos = 1;
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
    marcas = ["Cualquiera"];
    $('#selectUnidad'+ i).empty();
    $('#selectUnidad'+ i).append('<option>Cualquiera</option>')
    $('#selectPack' + i).empty();
    $("#selectUnidad"+i).attr("disabled",true);
    $("#magnitudExacta"+ i).attr("disabled",true);
    $("#selectPack"+i).attr("disabled",true);
    $("#packExacto"+i).attr("disabled",true);
    $("#inputCantidad"+i).attr("disabled",true);
    $("#addButton").attr("disabled",true);
    $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        prod: $('#input' + i).val(),
      }, function(data) {
            for(var j = 0; j < data.length; j++){
                
                var json = data[j];
                if (marcas.indexOf(json.marca) == -1 && json.marca.length != 0){
                     marcas.push (json.marca);
                };
            }
            marcas = marcas.sort();
            for (var j=0; j < marcas.length; j++){
				var marca = marcas[j];
				marca = marca.toLowerCase().replace( /\b\w/g, function (word) {
					return word.toUpperCase();
				});
                $('#selectMarca' + i).append('<option>'+ marca +'</option>');
            }
            $("#selectMarca"+i).attr("disabled",false);
          
      });    
};

getMarket = function(){
    if ((cantCampos == 1) && (!$('#input1').val()))
		alert("Debe seleccionar al menos un producto");
	else {
		var market = [];
		for (var i=1 ; i<=cantCampos; i++){
			var json = new Object();
			json.nombre = $('#input' + i).val();
			json.marca = $('#selectMarca' + i).val();
			json.unidadWeb = $('#selectUnidad' + i).val();
			json.packpor = $('#selectPack' + i).val().substring(1,$('#selectPack' + i).val().length);
			json.magnitudExacta = ($('#magnitudExacta' + i).prop('checked'));
			json.packExacto = ($('#packExacto' + i).prop('checked'));
			json.cantidad = $('#inputCantidad' + i).val()
			market.push(json);
		}
		var datos = new Object();
		datos.market = market
		$.ajax({
				url: '/getMarket',
				data: JSON.stringify(datos),
				type: 'POST',
				contentType: 'application/json',
				success: function(response) {
					sessionStorage.setItem("carrito",response);
					window.location.href = "resultado.html";
				},
				error: function(error) {
					console.log(error);
				}
		})
    }
};

// $("#selectMarca1").click(function(){
setMarca = function(i){
    $('#selectUnidad'+ (i)).empty();
    unidades = ["Cualquiera"];
    $('#selectPack' + (i)).empty();
    $("#selectPack"+(i)).attr("disabled",true);
    $("#packExacto"+(i)).attr("disabled",true);
    $("#inputCantidad"+(i)).attr("disabled",true);
    $("#addButton").attr("disabled",true);
    $.getJSON($SCRIPT_ROOT + '/datosPorProducto', {
        prod: $('#input' + (i)).val(),
        marca: $('#selectMarca' + (i)).val(),
      }, function(data) {
            for(var j = 0; j < data.length; j++){
                var json = data[j];
                if (unidades.indexOf(json.unidadWeb) == -1 && json.unidadWeb.length != 0){
                     unidades.push (json.unidadWeb);
                };
            }

            function sortNumber(a,b) {
            	a = a.replace(".","0.")
            	b = b.replace(".","0.")
			    return parseInt(a) - parseInt(b);
			}
            unidades = unidades.sort(sortNumber);
            for (var j=0; j < unidades.length; j++){
                $('#selectUnidad' + i).append('<option>'+ unidades[j] +'</option>');
            }
            $("#selectUnidad"+(i)).attr("disabled",false);
            $("#magnitudExacta"+(i)).attr("disabled",false);
          
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
                var json = data[j];
                if (packs.indexOf('x' + json.packpor) == -1 && json.packpor.length != 0){
                     packs.push ('x' + json.packpor);
                };
            }
            function sortNumber(a,b) {
            	a = a.replace("x","")
            	b = b.replace("x","")
			    return parseInt(a) - parseInt(b);
			}
            packs = packs.sort(sortNumber)
            for (var j=0; j < packs.length; j++){
                $('#selectPack' + (i)).append('<option>'+ packs[j] +'</option>');
            }
            $("#selectPack"+i).attr("disabled",false);
            $("#packExacto"+i).attr("disabled",false);
          
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
	$('#formProductos td:last select').append('<option>Cualquiera</option>');
	
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
	$('#selectUnidad'+(i+1)).append('<option>Cualquiera</option>')

	
	var inputmagnitudExacta = document.createElement('input');
	inputmagnitudExacta.id = 'magnitudExacta'+ (i+1);
	inputmagnitudExacta.type = 'checkbox';
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos td:last').append(inputmagnitudExacta);
	$('#packExacto'+(i+1)).attr('disabled',true);
	
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
	
	var inputpackExacto = document.createElement('input');
	inputpackExacto.id = 'packExacto'+ (i+1);
	inputpackExacto.type = 'checkbox';
	
	$('#formProductos tr:last').append('<td></td>');
	$('#formProductos td:last').append(inputpackExacto);
	$('#packExacto'+(i+1)).attr('disabled',true);	
	
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
	
	cantCampos = cantCampos + 1;
    marcas = [];
    packs = [];
    unidades = [];
	$("#addButton").attr("disabled",true);
    $('#addButton').attr("onClick","addFields("+(i+1)+")");
    
};
