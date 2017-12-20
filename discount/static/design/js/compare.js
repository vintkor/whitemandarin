$(document).ready(function(){
	$('.to-compare input').click(function(){
		toCompare($(this));
	})
	toCompare();
})

var add_to_compare_text = "К сравнению";

function toCompare(inputCheck){

	var data = {};
	if (inputCheck){
		id = $(inputCheck).val();

		if (!$(inputCheck).is(':checked')){

			$('.prod_wrap[data-id="' + id + '"] .to-compare__add').html(add_to_compare_text);
			$('.product-info .to-compare__add').html(add_to_compare_text);
			$('.slider_item .to-compare__add').html(add_to_compare_text);
			// alert('we are here');
		}

		data['id'] = id;
		
	}
	// alert(id);
	jQuery.ajax({
        url:'/compare/?i='+Math.random(),
        type:'post',
        dataType:'json',
        data:data,
        success:function(data)
        {
        	renderSuccessCompare(data);
        	// alert(compare_count);
        }
    })
}

function renderSuccessCompare(items){
    // alert(items.length);

    // alert(items[category_id].length);
    var count_id = 0;

    if (!window.category_id){
    	category_id = 0;
    }

    if (items[category_id]) {
    	count_id = items[category_id].length;
    }

	var text;
	var qt_compare = 0;
	var qt_compare_list = 0;
	var category_id = 0;

	for (var item in items){
		// console.log(items[item].length);
		qt_compare += items[item].length

		if (items[item].length >= 2){

			qt_compare_list += 1;
			category_id = item;
			text = '<a href="/to-compare/' + item + '/" class="to-compare__link">В сравнении</a>'
			text_count = '<a href="/to-compare/' + item + '/"  id="compare-total">Сравнение товаров (' + count_id + ')</a>'
		
		} else {

			text = add_to_compare_text;
			text_count = '<a href="javascript:;" id="compare-total">Сравнение товаров (' + count_id + ')</a>'

		}

		_.each(items[item], function(one){
			$('.prod_wrap[data-id="' + one + '"] .to-compare__add').html(text);
			$('.prod_wrap[data-id="' + one + '"] .to-compare input').attr('checked', 'checked');
			$('.product-info[data-id="' + one + '"] .to-compare__add').html(text);
			$('.product-info[data-id="' + one + '"] .to-compare input').attr('checked', 'checked');
			$('.slider_item[data-id="' + one + '"] .to-compare__add').html(text);
			$('.slider_item[data-id="' + one + '"] input').attr('checked', 'checked');
		});

		if (item == category_id){
			$('.product-compare').html(text_count);
		}
	}

	// console.log(qt_compare);
	if (qt_compare) {
		$('.top-compare .qty').html(qt_compare);
		$('.compare-lnk-sm .qty').html(qt_compare);
		$('.top-compare').addClass('active');
		$('.compare-lnk-sm').addClass('active');
	} else {
		$('.top-compare').removeClass('active');
		$('.compare-lnk-sm').removeClass('active');
	}

	// Создаем список сравнений
	if (qt_compare_list > 1) {
		var onetemplate = _.template($('#compare_category').html());
		// console.log('compare_list');

		$('.top-compare__lnk, .compare-lnk-sm').attr('href', '');
		$('.top-compare__lnk, .compare-lnk-sm').attr('data-toggle', 'dropdown');
		// $('.top-compare__lnk, .compare-lnk-sm').attr('data-target', '#compareModal');
		jQuery.ajax({
	        url:'/compare_list/?i='+Math.random(),
	        type:'post',
	        dataType:'json',
	        // data:data,
	        success:function(items)
	        {
				if (items){
					$('.compare-dropdown__list').html('');

					_.each(items, function(item){

						$('.compare-dropdown__list').append(onetemplate(item));

					});
				}
	        }
	    })
	}
	// Или создаем ссылку на сравнение в одной категории
	else {
		// console.log('compare_id');
		if (category_id) {
			$('.top-compare__lnk, .compare-lnk-sm').attr('href', '/to-compare/' + category_id + '/');
		} else {
			$('.top-compare__lnk, .compare-lnk-sm').attr('href', 'javascript:;');
		}
		$('.top-compare__lnk, .compare-lnk-sm').attr('data-toggle', '');
		$('.top-compare__lnk, .compare-lnk-sm').attr('data-target', '');

	}

}

function scroll(){
	$('.compare').addClass('scroll');
}

function compareRemove(item_id, category_id){

	$.ajax({
        url:'/to-compare/' +category_id+ '/?i='+Math.random(),
        type:'post',
        data:{
        	'item_id':item_id, 
        },
        success:function(count_id)
        {
        	if (count_id < 2){
        		var link = $('a.compare__add-btn').attr('href');
        		window.location.replace(link);
        	}
        	else {
        		$('td[data-id="' + item_id + '"]').remove();
        		$('td[data-property="' + item_id + '"]').remove();
        	}
        	if ($('.compare__filter-differences.active').length){
        		differencesProperties();
        	}
        }
    })
}

function differencesProperties(){
	console.log('differencesProperties');
	$('.compare__filter-all').removeClass('active');
	$('.compare__filter-differences').addClass('active');
	
	$('.compare__body tbody tr').each(function(){
		var tr = $(this),
		compare = true, temp = false, i = 0;

		$(this).find('td').each(function(){
			if (i > 0){
				if (temp != $(this).html()){
					compare = false	
				}
			}

			temp = $(this).html();
			i++;

		})

		if (compare == true){
			tr.addClass('hidden');
		}
	});
}

function allProperties() {
	console.log('allProperties');

	$('.compare__filter-differences').removeClass('active');
	$('.compare__filter-all').addClass('active');

	$('tr.hidden').removeClass('hidden');
}
