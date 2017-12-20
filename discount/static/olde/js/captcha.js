var clear, olditems = [], first = true;
$(document).ready(function(){
	clear = setInterval(function(){
		$.get('/writecaptcha/', function(items){
			console.log(olditems, items);

			if (!first && olditems.length != items.length){
				var audio = new Audio('/static/my.mp3');
				audio.play();
			}

			$('tbody').empty();
			if (items){
				$.each(items, function(i, item){
					$('tbody').append('<tr><td><img src="/media/captcha/' + item.request +'.jpg" alt=""></td><td><input type="text" name="response_' + item.id + '"></td></tr>');

				});
			}
			first = false;
			olditems = items;
		}, 'JSON')
	}, 6000)

	$('body').on('click','input',function(){

		// alert('we ARE HERE');
		clearInterval(clear);
	})
});
