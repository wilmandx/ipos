var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substrRegex;
    // an array that will be populated with substring matches
    matches = [];
    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');
    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push({ value: str });
      }
    });
 
    cb(matches);
  };
};
 
var clientes = ['Hector Naranjo Gallego', '10010133', 'Wilman Tello', '12345544'
];

$(document).ready(function(){
	iniciarInterfazPrincipal();
	iniciarVentas();
});


function iniciarInterfazPrincipal(){
	$('#btn-menu-collapser').click(
		function(){
			$('#navigation').toggle(
				function(){
					if($('#navigation').is(':hidden')){
			        	$('#page-wrapper').css('margin','0 0');
				    }else{
				        $('#page-wrapper').css('margin','0 0 0 250px');
				    } 						
				}
			);
			
		}
	);
}

function iniciarVentas(){
	/**Typeahead para los clientes***************************/
	var clientesRemote = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('nombre_completo'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  remote: '/ventas/clientes/?q=%QUERY'
	});
	clientesRemote.initialize();
	$('#cliente_p.typeahead').typeahead(null, {
	  name: 'clientes',
	  displayKey: 'nombre_completo',
	  source: clientesRemote.ttAdapter()
	}).bind('typeahead:selected', function(obj, datum) {
        $('#idcliente_p').val(datum.id);
    	//$('#vendedor_p').focus();
    });
	/****************************************************/

	/**Typeahead para los vendedores***************************/
	var vendedoresRemote = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('nombre_completo'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  remote: '/ventas/vendedores/?q=%QUERY'
	});
	vendedoresRemote.initialize();
	$('#vendedor_p.typeahead').typeahead(null, {
	  name: 'vendedores',
	  displayKey: 'nombre_completo',
	  source: vendedoresRemote.ttAdapter()
	}).bind('typeahead:selected', function(obj, datum) {
        $('#idvendedor_p').val(datum.id);
    });
	/****************************************************/

	/****Typeahead de los codigos de productos******************/
	var prodRemote = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('codigo'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  remote: '/ventas/codproducto/?q=%QUERY'
	});
	prodRemote.initialize();
	$('#n_producto_p.typeahead').typeahead(null, {
	  name: 'productos',
	  displayKey: 'codigo',
	  templates: {
	        suggestion: function (item) {
	            return '<p>' + item.codigo + ' - '+item.nombre+'</p>';
	        }
	  },
	  source: prodRemote.ttAdapter()
	}).bind('typeahead:selected', function(obj, datum) {
        $('#n_producto_p').val(datum.codigo);
    	$('#producto_p').val(datum.nombre);
    	$('#unitario_p').val(datum.valorVenta);
    	$('#valort_p').val(datum.valorVenta);
    	$('#valori_p').val(datum.iva);
    	$('#idproducto_p').val(datum.id);
    	$('#cantidad_p').focus().select();
    });
	/*******************************************************/
	/****Typeahead de los nombres de productos******************/
	var nameProdRemote = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('nombre'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  remote: '/ventas/nomproducto/?q=%QUERY'
	});
	nameProdRemote.initialize();
	$('#producto_p.typeahead').typeahead(null, {
	  name: 'productos_name',
	  displayKey: 'nombre',
	  templates: {
	        suggestion: function (item) {
	            return '<p>' + item.codigo + ' - '+item.nombre+'</p>';
	        }
	  },
	  source: nameProdRemote.ttAdapter()
	}).bind('typeahead:selected', function(obj, datum) {
        $('#n_producto_p').val(datum.codigo);
    	$('#producto_p').val(datum.nombre);
    	$('#unitario_p').val(datum.valorVenta);
    	$('#valort_p').val(datum.valorVenta);
    	$('#valori_p').val(datum.iva);
    	$('#idproducto_p').val(datum.id);
    	$('#cantidad_p').focus();
    });
	/*******************************************************/

	$('#btn-registrar-maestro').click(
		function(){
			savePedido();
		}
	);
	$('#btn-add-detalle').click(
		function(){
			saveDetalle();
		}
	);
	$('#btn-imprimir').click(
		function(){
			Print('facturita');
		}
	);
	$('#cantidad_p').keyup(function() {
	  cantidad=parseInt($(this).val());
	  $('#valort_p').val(cantidad*parseInt($('#unitario_p').val()));
	});
	eventosDetalleFactura();
	
		
}

function eventosDetalleFactura(){
	$('.btn-editItem').click(
		function(){
			loadDetalle($(this));
		}
	);
	$('.btn-delItem').click(
		function(){
			deleteDetalle($(this));
		}
	);
	$('.btn-obserItem').click(
		function(){
			Print();
			//observacionDetalle();
		}
	);
}

function savePedido(){
	//labelButton=$(this).get();
	ajax=$.post( "/ventas/save/", $("#frm-maestro").serialize());
	ajax.done(function( data ) {
    	//var factura = JSON.parse(data);
    	$("#idFactura").val(data.nroFactura);
    	//$("#factura").val(data.nroFactura);
    	$("#idFacturaD").val(data.nroFactura);
    	$("#fecha").val(data.fechaVenta);
    	$("#hora").val(data.horaVenta);
  	});
  	ajax.fail(function(data) {
  		alert('Error');
  	});
}

function saveDetalle(){
	var idFactura=0;
	idFactura=$("#idFactura").val();
	if(!idFactura){
		alert('No ha guardado aun el pedido por primera vez');
		return;
	}
	ajax=$.post( "/ventas/saveDetalle/", $("#frm-detalle").serialize());
	ajax.done(function( data ) {
		//Agregar el item a la tabla...
    	codigo=$('#n_producto_p').val();
    	idProducto=$('#idproducto_p').val();
    	producto=$('#producto_p').val();
    	cantidad=$('#cantidad_p').val();
    	descuento=$('#descuento_p').val();
    	valor=$('#unitario_p').val();
    	iva=$('#valori_p').val();
    	if(iva=='' || iva=='0')
    		iva='100';
    	iva=parseInt(iva);
    	total=parseInt(cantidad)*parseInt(valor)-parseInt(descuento);
    	valorSubtotal=(total*iva)/100;
    	var tr = $('<tr />');
    	tr.append($('<td />').html('<spam class="hide">'+data.idDetalle+'</spam><spam class="hide">'+idProducto+'</spam><spam>'+codigo+'</spam>'));
    	tr.append($('<td />').html(producto));
    	tr.append($('<td />').html(cantidad));
    	tr.append($('<td />').html('<spam>$</spam><spam>'+descuento+'</spam>'));
    	tr.append($('<td />').html('<spam>$</spam><spam>'+valor+'</spam>'));
    	tr.append($('<td />').html('<spam>'+iva+'</spam><spam>%</spam>'));
    	tr.append($('<td />').html('<spam>$</spam><spam>'+total+'</spam>'));
    	btnes='<button type="button" class="btn-editItem btn btn-default btn-sm">'+
                      '<span class="glyphicon glyphicon-edit"></span></button>&nbsp;'+
                    '<button type="button" class="btn-delItem btn btn-default btn-sm">'+
                      '<span class="glyphicon glyphicon-trash"></span></button>&nbsp;'+
                    '<button type="button" class="btn-obserItem btn btn-default btn-sm">'+
                      '<span class="glyphicon glyphicon-eye-open"></span></button>';
    	tr.append($('<td />').html(btnes));
    	$('#tbl-detalles').prepend(tr);
    	//Actualizar el gran total
    	grantotal=parseInt($('#tbl-detalles tr.total td:nth-child(2)').children()[1].innerHTML)+total;
    	granSubTotal=parseInt($('#tbl-detalles tr.subtotal td:nth-child(2)').children()[1].innerHTML)+valorSubtotal;
    	$('#tbl-detalles #td-maestro-subtotal').html('<strong>$</strong><strong>'+granSubTotal+'.00</strong>');
    	$('#tbl-detalles #td-maestro-iva').html('<strong>$</strong><strong>'+(grantotal-granSubTotal)+'.00</strong>');
    	$('#tbl-detalles #td-maestro-total').html('<strong>$</strong><strong>'+grantotal+'.00</strong>');

    	$('#frm-detalle').each (function(){
		  this.reset();
		});
		$('#n_producto_p').focus().select();
		eventosDetalleFactura();
	});
	ajax.fail(function( data ) {
  		alert('Error');
  	});
}
function loadDetalle(boton){
	tr=boton.parent().parent();
	
	$('#iddetalle_p').val($(tr.children()[0]).children()[0].innerHTML);
	$('#idproducto_p').val($(tr.children()[0]).children()[1].innerHTML);
	$('#n_producto_p').val($(tr.children()[0]).children()[2].innerHTML);

	$('#producto_p').val(tr.children()[1].innerHTML);
	$('#cantidad_p').val(tr.children()[2].innerHTML);
	$('#descuento_p').val($(tr.children()[3]).children()[1].innerHTML);
	$('#unitario_p').val($(tr.children()[4]).children()[1].innerHTML);
	$('#valori_p').val($(tr.children()[5]).children()[0].innerHTML);
	$('#valort_p').val($(tr.children()[6]).children()[1].innerHTML);
	
	$('#cantidad_p').focus().select();
}

function deleteDetalle(boton){
	tr=boton.parent().parent();
	idDetalle=$(tr.children()[0]).children()[0].innerHTML;
	ajax=$.get("/ventas/deleteDetalle/"+idDetalle+"/");
	ajax.done(function( data ) {
    	tr.fadeOut("slow", function () {
            tr.remove();
        });
  	});
  	ajax.fail(function(data) {
  		alert('Error');
  	});
}

function Print(div_id) {
   var printWin = window.open('', '', 'left=0,top=0,width=300,height=600,status=0');
    var toPrint = document.getElementById(div_id).innerHTML;
    printWin.document.open();
    printWin.document.write(toPrint);
    printWin.document.close();
    printWin.focus();
    printWin.print(true);
    printWin.close();
    console.log('imprimir...');
    return false;
}