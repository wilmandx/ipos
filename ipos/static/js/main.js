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
	});

	$('#vendedor_p.typeahead').typeahead(null, {
	  name: 'vendedores',
	  displayKey: 'nombre_completo',
	  source: clientesRemote.ttAdapter()
	});
	/****************************************************/

	/****Typeahead de los productos**********************/
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
		
}
function savePedido(){
	ajax=$.post( "/ventas/save/", $("#frm-maestro").serialize());
	ajax.done(function( data ) {
    	//var factura = JSON.parse(data);
    	$("#idFactura").val(data.nroFactura);
    	$("#factura").val(data.nroFactura);
    	$("#idFacturaD").val(data.nroFactura);
    	$("#fecha").val(data.fechaVenta);
    	$("#hora").val(data.horaVenta);
  	});
  	ajax.fail(function( data ) {
  		alert('Error');
  	});
  	grantotal=0;
  	granSubTotal=0;
}

function saveDetalle(){
	ajax=$.post( "/ventas/saveDetalle/", $("#frm-detalle").serialize());
	ajax.done(function( data ) {
		//Agregar el item a la tabla...
    	codigo=$('#n_producto_p').val();
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
    	tr.append($('<td />').html(codigo));
    	tr.append($('<td />').html(producto));
    	tr.append($('<td />').html(cantidad));
    	tr.append($('<td />').html(descuento));
    	tr.append($('<td />').html(valorSubtotal));
    	tr.append($('<td />').html(total-valorSubtotal));
    	tr.append($('<td />').html(total));
    	$('#tbl-detalles').prepend(tr);
    	//Actualizar el gran total
    	grantotal=grantotal+total;
    	granSubTotal=granSubTotal+valorSubtotal;
    	$('#tbl-detalles #td-maestro-subtotal').html('<strong>$'+granSubTotal+'.00</strong>');
    	$('#tbl-detalles #td-maestro-iva').html('<strong>$'+(grantotal-granSubTotal)+'.00</strong>');
    	$('#tbl-detalles #td-maestro-total').html('<strong>$'+grantotal+'.00</strong>');

    	$('#frm-detalle').each (function(){
		  this.reset();
		});
		$('#n_producto_p').focus();
	});
	ajax.fail(function( data ) {
  		alert('Error');
  	});
}