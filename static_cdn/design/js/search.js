$(document).ready(function(){
	$('.dropdown__search-cat a').click(function(){
		$('.dropdown__search-cat li').removeClass('active');
		$(this).parent().addClass('active');
		$('.activecat').html($(this).html());
		$('input[name="category_id"]').val($(this).data('id'));
		$('input[name="search"]').trigger('keydown');
	});

	$('input[name="search"]').keydown(function (event)
    {
  //   	var UP = 38;
		// var DOWN = 40;
		// var ENTER = 13;

		// // var getKey = function(e) {
		// //   if(window.event) { return e.keyCode; }  // IE
		// //   else if(e.which) { return e.which; }    // Netscape/Firefox/Opera
		// // };
		// // var keycode = (event.keyCode ? event.keyCode : event.which);

		// console.log(event);
		// return;

		// var keynum = e.keyCode;

		// console.log(keynum);
		// getKey(e);

		// if(keynum === UP) {
		//   //Move selection up
		//   console.log('oppo');
		//   return;
		// }

		// if(keynum === DOWN) {
		//   //Move selection down
		// }

		// if(keynum === ENTER) {
		//   //Act on current selection
		// }
        var startcounting, template = _.template($('#one-item-search').html());
        return function ()
        {

			$('.form-top-search').removeClass('active');
            if (startcounting) clearTimeout(startcounting);
            startcounting = setTimeout(function ()
            {
            	var search = $('input[name="search"]').val();

            	if (search.length > 1){

            		var data = {};
            		data.search = search;
            		if (parseInt($('input[name="category_id"]').val())){
            			data.category_id = $('input[name="category_id"]').val();
            		}

            		$.get('/search/', data, function(success){
            			if (success.length){
            				$('.smart-search-wrap').removeClass('hidden');
	            			$('.form-top-search').addClass('active');
	            			$('.list-group').empty();
	            			_.each(success, function(item){
		            			$('.list-group').append(template(item));
	            			})
            			}
            		}, 'JSON');

            	}
                // console.log('1') //put your ajax here.
            }, 500);
        }
    }()
    );

});
