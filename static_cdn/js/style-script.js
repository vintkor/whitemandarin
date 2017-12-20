function setActiveCatalog(){
    $('a[href="/catalog/"]').parent().addClass("active");
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    
    //Check to see if the window is top if not then display button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });
    
    //Click event to scroll to top
    $('.scrollToTop').click(function(){
        $('html, body').animate({scrollTop : 0},800);
        return false;
    });
    
});


(function ($) {

    $.fn.smplmnu = function (options) {

        //settings
        var settings = $.extend({
            // These are the defaults.
            speed: "0.5s"
        }, options);


        var hittrigger = $(this);
        var clspos = $('.menu-block');
        var overllay = '<div class="overally"></div>';

        $('body').prepend(overllay);


        //functions and methods
        hittrigger.click(function (event) {
            $('.menu-block').addClass('mnuopn');
            $('.mnuopn').css({
                'z-index': '999999',
                'transition': settings.speed
            });
            $('.overally').addClass('ovrActv');
            $("body").addClass("body-overflow");
        });

        $('.mnuclose').click(function (event) {
            clspos.removeClass('mnuopn');
            $('.overally').removeClass('ovrActv');
            $("body").removeClass("body-overflow");
        });

        $('.overally').click(function (event) {
            clspos.removeClass('mnuopn');
            $(this).removeClass('ovrActv')
            $("body").removeClass("body-overflow");
        });

        return this

    };

}(jQuery));


$('.toogle-menu').smplmnu();

(function ($) {

    $.fn.aside = function (options) {

        //settings
        var settings = $.extend({
            // These are the defaults.
            speed: "0.5s"
        }, options);


        var hittrigger = $(this);
        var clspo = $('.aside-filters');


        //functions and methods
        hittrigger.click(function (event) {
            $('.aside-filters').addClass('asdopn');
            $('.asdopn').css({
                'z-index': '999999',
                'transition': settings.speed
            });
            $('.overally').addClass('ovrActv');
            $("body").addClass("body-overflow");
        });

        $('.overally').click(function (event) {
            clspo.removeClass('asdopn');
            $(this).removeClass('ovrActv')
            $("body").removeClass("body-overflow");
        });

        return this

    };

}(jQuery));


$('.toogle-filters').aside();

(function ($) {

    $.fn.asidecart = function (options) {

        //settings
        var settings = $.extend({
            // These are the defaults.
            speed: "0.5s"
        }, options);


        var hittrigger = $(this);
        var clspo = $('.cart-aside');


        //functions and methods
        hittrigger.click(function (event) {
            $('.cart-aside').addClass('asdopn');
            $('.asdopn').css({
                'z-index': '999999',
                'transition': settings.speed
            });
            $('.overally').addClass('ovrActv');
            $("body").addClass("body-overflow");
        });

        $('.overally').click(function (event) {
            clspo.removeClass('asdopn');
            $(this).removeClass('ovrActv')
            $("body").removeClass("body-overflow");
        });

        return this

    };

}(jQuery));


$('.toogle-cart').asidecart();

$(".toggle-search").click(function(e){
    e.preventDefault();
    $(".search-block").slideToggle("fast");
});


$('body').on('click','.btn-number', function(e){
    e.preventDefault();

    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {

            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            }
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});

$('body').on('focusin', '.input-number',function(){
   $(this).data('oldValue', $(this).val());
});

$('body').on('change', '.input-number', function() {

    minValue =  parseInt($(this).attr('min'));
    maxValue =  parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());

    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }


});

$('body').on("keydown", ".input-number", function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
         // Allow: Ctrl+A
        (e.keyCode == 65 && e.ctrlKey === true) ||
         // Allow: home, end, left, right
        (e.keyCode >= 35 && e.keyCode <= 39)) {
             // let it happen, don't do anything
             return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});



function end_ov(num) {
    // console.log(num);
    var end = '';
    if (num < 11 || num > 14) {
        switch (num % 10) {
            case 0:
                end = "ов";
                break;
            case 1:
                break;
            case 2:
                end = "а";
                break;
            case 3:
                end = "а";
                break;
            case 4:
                end = "а";
                break;
            case 5:
                end = "ов";
                break;
            case 6:
                end = "ов";
                break;
            case 7:
                end = "ов";
                break;
            case 8:
                end = "ов";
                break;
            case 9:
                end = "ов";
                break;
            case 10:
                end = "ов";
                break;
        }
    } else if (num >= 11 || num <= 14) {
        end = "ов";
    }
    // console.log(end);
    return end;
}



$(document).ready(function(){

    // smartValue();
      $('.addcomments').submit(function(e){
        e.preventDefault();

        $.post('/addcomments/', $(this).serialize(), function(){
            $('.addcomments').html('<b>Ваш комментарий был добавлен, после модерации он будет доступен!</b>')
        })
    });

      $('select.filter').change(function(){
        $('form.filters').submit();
      })


    $('.login-form').submit(function(e){
        e.preventDefault();
        var request = $.ajax({
          url: '/accounts/login/',
          method: "POST",
          data: {csrfmiddlewaretoken: getCookie('csrftoken'), login: $('#login-user').val(), password: $('#login-password').val()},
          dataType: "html"
        });

        request.done(function(msg) {
            location.reload();
        });

        request.fail(function( jqXHR, textStatus ) {
            $('.login-error').removeClass('hidden');
        });
    });


    $('.register-form').submit(function(e){

        e.preventDefault();
        var email = $('#email').val(),
            password1 = $('#reg-password').val(),
            password2 = $('#reg-password2').val();

        if (email && password1 && password2 && password1==password2) {
            var request = $.ajax({
              url: '/accounts/signup/',
              method: "POST",
              data: {csrfmiddlewaretoken: getCookie('csrftoken'), username: email, email: email, password1: password1, password2: password2},
              dataType: "html"
            });

            request.done(function(msg) {
                $('.register-form').addClass('hidden');
                $('.register-success').removeClass('hidden');
                // location.reload();
            });

            request.fail(function( jqXHR, textStatus ) {
                $('.register-error').removeClass('hidden');
            });

        } else {

            $('.register-error').removeClass('hidden');

        }
    });


    $('.addemail').submit(function(e){
        e.preventDefault()
        $.post('/addemail/', $(this).serialize(), function(success){
            alert(success);
        });
    });
    $('.oneclick').submit(function(e){

        e.preventDefault();
        var phone = $('input[name="phone"]').val();

        if (!phone){
            $('input[name="phone"]').css("border","1px solid red");
        }

        $.post('/oneclick/', $(this).serialize(), function(success){
            $('.oneclick').addClass('hidden');
            $('.thank-form').removeClass('hidden');
        });
    });


    $('.watchlist').click(function(e){
        var id = $(this).data('id'), img = $(this).find('img');
        if (id){
            $.post('/profile/addtowishlist/', {id: id}, function(success){
                if (img.attr('src') == "/static_cdn/images/icons/watchlist.png"){
                    img.attr('src', '/static_cdn/images/icons/on-watchlist.png');
                } else {
                    img.attr('src', '/static_cdn/images/icons/watchlist.png');
                }
                // product.toggleClass('whishlist-active');
            });
        }
    });

    $('.to-cart').click(function(){
        var id = $('input[name="product_id"]').val(),
            count = $('input[name="quant2"]').val(),
            data = {
                id: id,
                count: count,
            };

        if ($('.mainsize').length){
            data['size'] = $('.mainsize').val();
        }

        $.post('/addtocart/', data, function(success){
            $('.bag-items').html(success);
            $('.bag-items').removeClass('hidden');
        });

    });

    $('.settingsform').submit(function(e){
        e.preventDefault();
        $.post('/profile/settings/', $(this).serialize(), function(){
            $('.saveok').removeClass('hidden');
        });
    });


});
