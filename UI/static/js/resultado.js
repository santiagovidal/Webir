$(document).ready(function() {
  carrito = JSON.parse(sessionStorage.carrito)
  productosTInglesa = carrito.tinglesa
  productosDevoto = carrito.devoto

  html = ""

  for (var i = 0; i < productosTInglesa.length; i++) {

    if (productosTInglesa[i].length > 0){
        html += "<tr class='filaTInglesa' id='tInglesaResultProduct"+ i + "'>"
        for (var j = 0; j < productosTInglesa[i].length; j++) {
            producto = productosTInglesa[i][j]
            
            html += "<td>"
            html += "<table align='center' class='resultProduct' value='"+ producto["cantidad"] + "'>"
            html += "<tr><td>" + producto["nombre"] + "</td></tr>"
            html += "<tr><td>" + producto["marca"] + "</td></tr>"
            html += "<tr><td>" + producto["unidadWeb"] + "</td></tr>"
            html += "<tr><td>x" + producto["packpor"] + "</td></tr>"
            html += "<tr><td>" + producto["cantidad"] + " unidades</td></tr>"
            html += "<tr><td id='price'>Precio unitario: $" + producto["precio"] + "</td></tr>"
            html += "</table>"
            html += "</td>"
        }
        // Se completan las columnas que falten en caso que haya menos de
        // 3 productos que matchearon
        for (var j = productosTInglesa[i].length; j < 3; j++) {
            html += "<td></td>"
        }
        html += "<td align='center'>$ 0</td>"
        html += "</tr>"
    }
  }

  $(".filaTInglesa").after(html)

  html = ""

  for (var i = 0; i < productosDevoto.length; i++) {

    if (productosDevoto[i].length > 0){
        html += "<tr class='filaDevoto' id='devotoResultProduct"+ i + "'>"
        for (var j = 0; j < productosDevoto[i].length; j++) {
            producto = productosDevoto[i][j]
            
            html += "<td>"
            html += "<table align='center' class='resultProduct' value='"+ producto["cantidad"] + "'>"
            html += "<tr><td>" + producto["nombre"] + "</td></tr>"
            html += "<tr><td>" + producto["marca"] + "</td></tr>"
            html += "<tr><td>" + producto["unidadWeb"] + "</td></tr>"
            html += "<tr><td>x" + producto["packpor"] + "</td></tr>"
            html += "<tr><td>" + producto["cantidad"] + " unidades</td></tr>"
            html += "<tr><td id='price'>Precio unitario: $" + producto["precio"] + "</td></tr>"
            html += "</table>"
            html += "</td>"
        }
        // Se completan las columnas que falten en caso que haya menos de
        // 3 productos que matchearon
        for (var j = productosDevoto[i].length; j < 3; j++) {
            html += "<td></td>"
        }
        html += "<td align='center'>$ 0</td>"
        html += "</tr>"
    }
  }

  $(".filaDevoto").after(html)
});

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