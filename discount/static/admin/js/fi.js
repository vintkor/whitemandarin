(function($){

	$(document).ready(function(){

		$('.y-items .col-2 img').click(function(){
			var i = 0;
			$('.y-items .col-2 img').removeClass('active');
			$(this).addClass('active');
			$('.y-items .col-2 img').each(function(){
				if ($(this).hasClass('active')){
					$('#id_yimage').val(i);
					return;
				}
				i++;
			});
		});

		$('.products input').click(function(){
			$('#id_product').val($(this).data('id'));
		});
		$('.categories input').click(function(){
			$('#id_category').val($(this).data('id'));
		});
		$('.brands input').click(function(){
			$('#id_brand').val($(this).data('id'));
		});



	});

})(django.jQuery);
