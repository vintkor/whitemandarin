function renderModal(item){
	var template = _.template($('#addproduct').html());
	// $('#createProductModal').modal('hide');
	$('#createProductModal').modal();
	$('#createProductModal .modal-body').empty();
	$('#createProductModal .modal-body').html(template(item));
}

$(document).ready(function(){

	$('input[type="button"]').click(function(){
		var search = $(this).closest('tr').find('input[type="text"]').val();
			s_id = $(this).closest('tr').data('id'),
			phraza = $(this).closest('tr').find('.nametext').html();;
		$('.modal-footer').addClass('hidden');
		$('.newresult2').addClass('hidden');

		$('#myModal .modal-title span').html(phraza);

		$.post('/simplesearch/', {q: search, s_id: s_id}, function(success){
			$('#myModal').modal();
			$('#myModal ul').empty();
			// $('#myModal ul.active').empty();
			_.each(success.active, function(item){

				$('#myModal ul.connect').append('<li><input class="connection" type="checkbox" checked="checked" data-id="' + item.id + '"/>' + item.name + '</li>')
			});

			_.each(success.items, function(item){

				$('#myModal ul.connect').append('<li><input class="connection" type="checkbox" data-id="' + item.id + '"/>' + item.name + '</li>')
			});


			_.each(success.newitems, function(item){

				$('#myModal ul.newitems').append('<li><input class="newproduct2" type="radio" name="newproduct2" value="' + item.id + '"/>' + item.name + '</li>')
			});

			_.each(success.fromprice, function(item){
				var active = '';
				if (item.active){
					active = ' checked="checked" '

				}


				$('#myModal ul.fromprice').append('<li><input class="connection2" type="checkbox" ' + active + ' data-id="' + item.id + '"/>' + item.name + '</li>');
			});

		}, "JSON")

		// alert(search, id);
	});

	$('#myModal').on('click', 'input[type="radio"]', function(){
		$('.modal-footer').removeClass('hidden');
	});

	$('#myModal').on('click', '.createproduct2', function(){
		var h_id = $('.newproduct2:checked').val(),
			data = {s_id: s_id, h_id: h_id};

		console.log('we are here');

		jQuery.ajax({
        type: "POST",
        async: true,
        url: '/newproduct2/',
        data:  data,
        // dataType: "json",
        // contentType: "application/json; charset=utf-8",
        success: function (msg) {
			$('.newresult2').removeClass('hidden');
			$('.newresult2').attr('href', msg);
               // alert(msg)
           },
        error: function (err)
        { alert(err.responseText)}
    });


	});
	$('#myModal').on('click', 'input[type="checkbox"].connection', function(){
		var c_id = $(this).data('id');
		$.post('/createconnection/', {s_id: s_id, c_id: c_id}, function(success){
			_.each(success, function(id){
				$('input.connection2[data-id="' + id + '"]').prop('checked', true);
			});
		});
		$('tr[data-id=' + s_id + ']').remove();
		console.log(s_id);
	});

	$('#myModal').on('click', 'input[type="checkbox"].connection2', function(e){
		var c_id = 0;
		var ns_id = $(this).data('id');

		if (!$('#myModal input[type="checkbox"].connection:checked').length){
			e.preventDefault();
			alert('Товар не связан');
			return;
		}
		c_id = $('#myModal input[type="checkbox"].connection:checked').data('id');

		$.post('/createconnection/', {s_id: ns_id, c_id: c_id});
		$('tr[data-id=' + ns_id + ']').remove();
		console.log(ns_id, c_id);
	});

	$('input.hotlineok').click(function(){

		var id = $(this).closest('tr').data('id');
		$.post('/hotlineok/', {id: id});


	});

	$('a.create').click(function(){

		var id = $(this).closest('tr').data('id');

		$.post('/getpricestr/', {id: id}, function(item){
			itemstr = item;
			renderModal(item);
		});

	});

	$('body').on('click', '.saveandparse', function(){

		var template = _.template($('#addproduct').html());

		var data = {
			'id': $('input[name="id"]').val(),
			'hotlineurl': $('input[name="hotlineurl"]').val(),
		}


		$.post('/saveandparse/', data, function(item){
			$('#createProductModal .modal-body').html(template(item));
			// renderModal(item);
		});

		console.log(data);

	});

	// $('body').on('click', '.connect', function(){

	// 	var data = {
	// 		'id': $('input[name="id"]').val(),
	// 		'cat': $('select[name="cat"]').val(),
	// 		'filter': $('select[name="filter"]').val(),
	// 	}

	// 	$.post('/connectproptocat/', data, function(item){
	// 		var template = _.template($('#addproduct').html());

	// 		$('#createProductModal .modal-body').html(template(item));


	// 		itemstr = item;
	// 		if (item.catconnected){
	// 			$('.connect').html('Развязать')
	// 		} else {
	// 			$('.connect').html('Связать')
	// 		}
	// 	});

	// });


	$('body').on('click', '.brandconnect', function(){

		var data = {
			'id': $('input[name="id"]').val(),
			'brand': $('select[name="brand"]').val(),
			'filterbrand': $('select[name="filterbrand"]').val(),
		}

		// console.log(data);

		$.post('/connectproptobrand/', data, function(item){
			if (item){
				$('.brandconnect').html('Развязать')
			} else {
				$('.brandconnect').html('Связать')
			}
		});

	});


	$('body').on('change', '.filtername', function(){
		var id = parseInt($(this).val()), self = this;

		if (id){
			_.each(itemstr.connect_filters, function(one){
				if (id==one.id){
					var text = ''
					_.each(one.items, function(it){
						text += "<option value='" + it.id +"'>" + it.name + "</option>";
					});
					text += "<option value='add'>Добавить новый</option>";
					$(self).closest('.form-group').find('.filteritem').html(text);
					// console.log($(self).closest('.form-group').length);
					return;
				}
			});
		} else {
			var text = '<option value="0">Выберите значение</option>';
			$(self).closest('.form-group').find('.filteritem').html(text);
		}

		$(self).closest('.form-group').find('.addfilteritem').addClass('hidden');



	});

		$('body').on('change', '.filteritem', function(){
			var id = $(this).val();

			if (id == 'add'){
				$(this).closest('.form-group').find('.addfilteritem').removeClass('hidden');
			} else {
				$(this).closest('.form-group').find('.addfilteritem').addClass('hidden');

			}

		});

		$('body').on('click', '.connectfiltername', function(){
			var cat = parseInt($("select[name='cat']").val()),
				ps_id = parseInt($("input[name='id']").val()),
				str_id = parseInt($(this).closest('.form-group').data('id')),
				f_id = parseInt($(this).closest('.form-group').find('.filtername').val()),
				data = {
					cat: cat,
					ps_id: ps_id,
					str_id: str_id,
					f_id: f_id,
				}, self = this;

				$.post('/connectfiltername/', data, function(success){
					console.log(parseInt(success));
					if (parseInt(success)){
						$(self).html('Развязать');
						$(self).addClass('success');
						$(self).closest('.form-group').css('background', '#FFFFE0');
					} else {
						$(self).html('Связать');
						$(self).removeClass('success');
						$(self).closest('.form-group').css('background', '#FFFFFF');
					}

				}, 'html');
		});


		$('body').on('click', '.connectfilteritem', function(){
			var cat = parseInt($("select[name='cat']").val()),
				ps_id = parseInt($("input[name='id']").val()),
				str_id = parseInt($(this).closest('.form-group').data('id')),
				fs_id = parseInt($(this).closest('.form-group').find('.filteritem').val()),
				data = {
					cat: cat,
					ps_id: ps_id,
					str_id: str_id,
					fs_id: fs_id,
				}, self = this;

				$.post('/connectfilteritem/', data, function(success){
					if (parseInt(success)){
						$(self).html('Развязать');
						$(self).addClass('success');
						$(self).closest('.form-group').css('background', '#98FB98');

					} else {
						$(self).html('Связать');
						$(self).removeClass('success');
						$(self).closest('.form-group').css('background', '#FFFFE0');
					}

				}, 'html');
		});


		$('body').on('click', '.connectproperty', function(){
			var cat = parseInt($("select[name='cat']").val()),
				ps_id = parseInt($("input[name='id']").val()),
				str_id = parseInt($(this).closest('.form-group').data('id')),
				p_id = parseInt($(this).closest('.form-group').find('.property').val()),
				data = {
					cat: cat,
					ps_id: ps_id,
					str_id: str_id,
					p_id: p_id,
				}, self = this;

				$.post('/connectproperty/', data, function(success){
					if (parseInt(success)){
						$(self).html('Развязать');
						$(self).addClass('success');
						$(self).closest('.form-group').css('background', '#98FB98');
					} else {
						$(self).html('Связать');
						$(self).removeClass('success');
						$(self).closest('.form-group').css('background', '#FFFFFF');
					}

				}, 'html');
		});


		$('body').on('change', 'select[name="color_id"]', function(){

			console.log($(this).val());
			if ($(this).val() == "addnew"){
				$('.colorhidden').removeClass('hidden');
			} else {
				$('.colorhidden').addClass('hidden');

				$('input[name="color"]').val($('select[name="color_id"] option:selected').html());

			}
		});



		$('body').on('submit', '.newproduct', function(e){
			e.preventDefault();

			$.post('/newproduct/', $(this).serialize(), function(success){
				// alert(123);
				console.log(success);
			    $('.newresult').removeClass('hidden');
			    $('.newresult').attr('href', success);

			}, 'html');

		});



});

function createnewproduct(sid, hid)
{
	var data = {s_id: sid, h_id: hid};

	console.log('we are here');

	jQuery.ajax({
    type: "POST",
    async: true,
    url: '/newproduct2/',
    data:  data,
    // dataType: "json",
    // contentType: "application/json; charset=utf-8",
    success: function (msg) {
		$('.cnp_' + sid).removeClass('hidden');
		$('.cnp_' + sid).attr('href', msg);
           // alert(msg)
       },
    error: function (err)
	    { alert(err.responseText)}
	});

}

// function createconnection(sid, cid){
// 		// var c_id = $(this).data('id');
// 		$.post('/createconnection/', {s_id: sid, c_id: cid}, function(){
// 			console.log('oke');
// 		});
// 	}
