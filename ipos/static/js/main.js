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

var productos = ['Gaseosa 350', 'Sopa de Maiz', 'Vino' 
]; 

var vendedor = ['Juan mario','Juan Carlos','Juan Pedro', 'Pedro', 'Luis', 'Maria'];

 $(document).ready(function(){
 		console.log('llega');
		$('#cliente_p .typeahead').typeahead({
		  hint: true,
		  highlight: true,
		  minLength: 2
		},
		{
		  name: 'clientes',
		  displayKey: 'value',
		  source: substringMatcher(clientes)
		});

		$('#codVendedor.typeahead').typeahead({
		  hint: true,
		  highlight: true,
		  minLength: 2
		},
		{
		  name: 'vendedor',
		  displayKey: 'value',
		  source: substringMatcher(vendedor)
		});
		$('#vendedor_p.typeahead').typeahead({
		  hint: true,
		  highlight: true,
		  minLength: 2
		},
		{
		  name: 'vendedor',
		  displayKey: 'value',
		  source: substringMatcher(vendedor)
		});
    
    $('#producto_p .typeahead').typeahead({
      hint: true,
      highlight: true,
      minLength: 2
    },
    {
      name: 'productos',
      displayKey: 'value',
      source: substringMatcher(productos)
    });    
});