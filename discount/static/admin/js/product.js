(function($){

	$(document).ready(function(){
		if ($('select#id_category').length){
			renderAll();
		}


		$('#id_category').change(function(){
			// alert("we are here");
			renderAll();
		});

	});

	function get_request_path(start, cat_id){

		var temp = window.location.href.split('/'),
			product_id = temp[temp.length - 3],
			path = '/'+ start + '/' + cat_id + '/';

		console.log(product_id);

		if (product_id > 0){
			path += product_id + '/';
		}

		return path;

	}

	function renderAll(){

		$('.allfilters').remove();
		$('.field-category').after('<div class="allfilters"><div class="filters"><h3>Фильтры</h3></div><div class="properties"><h3>Свойства</h3></div><hr /></div>');

		searchfilteraction();
		searchpropertyaction();

	}


	function searchfilteraction(){

		var cat_id = $('#id_category').val(),
			path = get_request_path('get_filters', cat_id),
			template = _.template($('#new_select').html());


		// console.log(path);

		if (cat_id){
			$.get(path, function(success){
				$('.allfilters .filters').html("<h3>Фильтры</h3>");
				// $('.field-category').after('<div class="allfilters"><div class="filters"><h3>Фильтры</h3></div><div class="properties"><h3>Свойства</h3></div><hr /></div>');

				_.each(success, function(one){
					$('.filters').append(template(one));
				});
				// searchpropertyaction(cat_id);
			});
		}

	}


	function searchpropertyaction(){
		var cat_id = $('#id_category').val(),
			path = get_request_path('get_properties', cat_id),
			template = _.template($('#new_property').html());

		// console.log(path);
//

		$.get(path, function(success){
			// console.log($('.allfilters .properties').length);
			$('.allfilters .properties').html("<h3>Свойства</h3>");

			// console.log(success);
			_.each(success, function(one){
				// console.log(template(one));
				$('.allfilters .properties').append(template(one));
			});
		});


	}



})(django.jQuery);
