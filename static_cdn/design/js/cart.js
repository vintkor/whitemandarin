$(document).ready(function(){
	$('.incart, .edit-order').click(function(){
		showCart('/show_cart/');
	});
    if ($('.checkout-container').length) {
    	showCart('/show_cart/');
        // console.log('checkout');
    }
    jQuery("input[name='phone']").mask("+38(099) 999-9999");

    $('form.oneclick').submit(function(e){
        e.preventDefault();

        var phone = jQuery("#oneclickModal input[name='phone']").val(),
            data = {
                phone: phone,
                product_id: $('input[name="product_id"]').val(),
            };

        if(!phone)
        {
            console.log(phone);
            jQuery("#oneclickModal input").css("border","1px solid red");
            return false;
        }
        else
        {
            jQuery("#oneclickModal input").css("border","1px solid #ccc");
        }

        // console.log();
        jQuery("#oneclickModal .modal-header").css('display', 'none');
        jQuery("#oneclickModal .modal-body").css('display', 'none');
        jQuery("#oneclickModal .modal-footer").css('display', 'none');
        jQuery("#oneclickModal .thank-form").show();
        // jQuery("#oneclickModal .thank-form").delay(5000).fadeOut('slow');


        // jQuery("#oneclickModal input").val("");

        jQuery.ajax({
            url:'/oneclick/?i='+Math.random(),
            type:'post',
            dataType:'html',
            data: data,
            success:function(data)
            {

            }
        });

    });


    $('form.notify-modal').submit(function(e){
        e.preventDefault();

        var phone = jQuery("#notifAvailModal input[name='phone']").val(),
            name = jQuery("#notifAvailModal input[name='name']").val(),
            email = jQuery("#notifAvailModal input[name='email']").val(),
            data = {
                phone: phone,
                name: name,
                email: email,
                product_id: $('input[name="product_id"]').val(),
            };
        // console.log();
        jQuery("#notifAvailModal .modal-header").css('display', 'none');
        jQuery("#notifAvailModal .modal-body").css('display', 'none');
        jQuery("#notifAvailModal .modal-footer").css('display', 'none');
        jQuery("#notifAvailModal .thank-form").show();
        // jQuery("#oneclickModal .thank-form").delay(5000).fadeOut('slow');


        // jQuery("#oneclickModal input").val("");

        jQuery.ajax({
            url:'/noclick/?i='+Math.random(),
            type:'post',
            dataType:'html',
            data: data,
            success:function(data)
            {

            }
        });

    });

    $('body').on('change', 'select[name="warehouse"]', function(){
        changeDelivery();
    });

    getCities();
});


function oneClick(product_id) {

    ga('send', 'event', 'button', 'click', 'buy1click');

}


function addToCart(id, color, name, category, sky, price){
    // ga('send', 'event', 'РљРѕСЂР·РёРЅР°', 'Р”РѕР±Р°РІРёР» РІ РєРѕСЂР·РёРЅСѓ', 'РљР»РёРє РІ РєР°СЂС‚РѕС‡РєРµ С‚РѕРІР°СЂР°');

    // ga('ecommerce:addTransaction', {
    //   'id': id,                     // Transaction ID. Required.
    //   'affiliation': '20k.com.ua',   // Affiliation or store name.
    //   'revenue': price,               // Grand Total.
    //   'shipping': 0,                  // Shipping.
    //   'tax': 0                     // Tax.
    // });

    // ga('ecommerce:addItem', {
    //   'id': id,                     // Transaction ID. Required.
    //   'name': name,    // Product name. Required.
    //   'sku': sky,                 // SKU/code.
    //   'category': category,         // Category or variation.
    //   'price': price,                 // Unit price.
    //   'quantity':'1'                   // Quantity.
    // });
    // ga('ecommerce:send');

    var path = '/add_to_cart/' + id + '/';

    if (parseInt(color) > 0){

        path += color + '/';

    }

    showCart(path);

}


function addComplect(id, color_id){

    var path = '/add_complect/' + id + '/';

    if (parseInt(color_id) > 0){

        path += color_id + '/';

    }

    showCart(path);
}


function showCart(path){
    // var carttemplate = _.template($('#cart-template').html());

    // $.colorbox({html: carttemplate(), width: "600px", height: "400px"});

    $.get(path, function(success){

        console.log(success);
        renderSuccess(success);

    },
    'JSON')
}


function renderSuccess(success){

    var onetemplate = _.template($('#one-item-template').html()),
        carttemplate = _.template($('#cart-item-template').html()),
        completctemplate = _.template($('#one-complect').html()),
        onecomplecttemplate = _.template($('#one-complect-item').html());

    if ($('#one-order-cart').length){
        var oneordercarttemplate = _.template($('#one-order-cart').html());
        $('.holder ul').empty();
    }

    // console.log(success);
    $('.cart-items .items, .checkout-container .items').empty();
    if (success.complects){

        _.each(success.complects, function(item){
            $('.cart-items .items, .checkout-container .items').append(completctemplate(item));
            if ($('.holder ul')) {
                $('.holder ul').append('<li>' + completctemplate(item) + '</li>');
            }

            _.each(item.items, function(one){
                $('.complect' + item.id + ' .complect_items').append(onecomplecttemplate(one));
            })
        });

    }

    // console.log(success.items);
    if (success.items){
        _.each(success.items, function(item){

            $('.cart-items .items').append(onetemplate(item));

            if (carttemplate.length){
                $('.checkout-container .items').append(carttemplate(item));
            }

        });
    }

    $('.incart .qty').html(success.allcount);
    $('.navbar-nav-cart-qty').html(success.allcount);
    $('.incart .qty').css('display', 'block');
    $('.navbar-nav-cart-qty').css('display', 'block');

    if (success.allcount) {
    	var allcount = success.allcount;
    	var allprice = success.allprice;
      var end = end_ov(allcount);
	    var title = allcount + " товар" + end + " на сумму " + allprice + " грн."
    } else {
	    var title = "Ничего не куплено!"
    }
    // console.log(title);
    $('.incart').attr('data-original-title', title);

    $('.summary, .total-count').html(success.allprice)

    $(".item_qty").bind('keyup mouseup', function () {
        console.log('item_qty');
        setTimeout(function(){
            $(".item_qty").unbind();
            $.post('/change_cart/', $('.items').serialize(), function(success){
                $('.items').empty();
                console.log('item_qty -> empty');
                renderSuccess(success);
            });
        }, 2000);
    });
}


// function top_cart(allcount, allprice) {
// 		if (allcount) {
//       var end = end_ov(allcount);
// 	    var title = allcount + " товар" + end + " на сумму " + allprice + " грн."
//     } else {
// 	    var title = "Ничего не куплено!"
//     }
//     // console.log(title);
//     $('.incart').attr('data-original-title', title);
// }


function removeItem(id) {
    $('input[name="quantity_' + id + '"]').val(0);
    recountCart();
}


function removeComplectItem(id) {
    $('input[name="complect_' + id + '"]').val(0);
    recountCart();
}


function recountCart(){
    $.post('/change_cart/', $('.items').serialize(), function(success){
        $('.items').html('');
        renderSuccess(success);
    });
}

function changeDelivery(){
    $('#delivery-service').val($( "select[name='city'] option:selected" ).text() + ' ' + $( "select[name='warehouse'] option:selected" ).text());

}

function getCities(){

    if ($('select[name="city"]').length) {
        $.get('/get_cities/', function(items){
            $('select[name="city"]').empty();
            _.each(items, function(item){
                $('select[name="city"]').append('<option value="'+ item.value + '">' + item.name + '</option>');
            });

            $('select[name="city"]').change(function(){
                getWarehouses($(this).val());
            });

            getWarehouses($('select[name="city"]').val());

        });
    };
}

function getWarehouses(city){

    $.post('/get_warehouses/', {city: city}, function(items){

        $('select[name="warehouse"]').empty();
        _.each(items, function(item){
            $('select[name="warehouse"]').append('<option value="'+ item.value + '">' + item.name + '</option>');
        });

        changeDelivery();
    });

}


// function deleteProduct(name){
//     $('input[name="' + name + '"]').val(0);
//     recountCart();
// }
