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
	/*$('#cliente_p.typeahead').typeahead({
		  hint: true,
		  highlight: true,
		  minLength: 2
		},
		{
		  name: 'clientes',
		  displayKey: 'value',
		  source: substringMatcher(clientes)
		});*/
	/*$('#cliente_p.typeahead').typeahead({
		  name: 'Search',
		  remote: '/search?query=%QUERY'
		});*/

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

	$('form #btn-add-product').click(
		function(){
			savePedido();
		}
	);
		
}
function savePedido(){
	ajax=$.post( "/ventas/save/", $("form[role=form]").serialize());
	ajax.done(function( data ) {
    	//var factura = JSON.parse(data);
    	$("#idFactura").val(data.nroFactura);
    	$("#Factura").val(data.nroFactura);
    	//Agregar el item a la tabla...
    	$('.table table-striped table-hover').append('<tr><td>XXXXXXXXXXXX</td></tr>');
    	//Actualizar el gran total
  	});
  	ajax.fail(function( data ) {
  		alert('Error');
  	});
}