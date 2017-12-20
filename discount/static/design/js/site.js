function filter() {
    var brand_qt = $('.filters__brand:checked').length,
        url = $('.filter__info').attr('data-url'),
        params = $('form.all-filters.other').serialize(),
        brand_params = $('form.all-filters.brand').serialize();

    // if (brand_qt == 1) {
    //     var brand_slug = $('.filters__brand:checked').attr('data-slug');
    //     url += brand_slug + '/';
    // } else {
    //     var brand_slug = '';
    // }

    // alert(123);

    if (params) {
        params = '?' + params;
        if (brand_qt > 0) {
            params += '&' + brand_params;
        }
    } else
    if (brand_qt > 0) {
        params += '?' + brand_params;
    } else {
        params = '';
    }

    // console.log(url + params);
    // return 0;

    window.location = url + params;
}


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


$(document).ready(function() {

    if ($('.navbar .dropdown-menu > li.active').length) {
        $('.navbar .dropdown-menu > li.active').parent().parent().addClass('active');
    }

    // $('div#navbar-collapse > ul > li > a').click(function(){
    //     location = $(this).attr('href');
    // });

    $(".reviews_num").each(function(i) {
        var num = $(this).attr('data-reviews');
        var id = $(this).attr('data-id');
        var end = end_ov(num);

        $('.reviews_end[data-id="' + id + '"]').html(end);
        // console.log(num);
    });

    $('.filters--price').change(function() {

        setTimeout(function() {

            if (max_price == parseInt($('.max_now').val())) {
                $('.max_now').remove();
            }

            if (min_price == parseInt($('.min_now').val())) {
                $('.min_now').remove();
            }

            filter();

        }, 1000)
    })

    $('form.all-filters.brand input:checkbox').click(function() {

        if (max_price == parseInt($('.max_now').val())) {
            $('.max_now').remove();
        }

        if (min_price == parseInt($('.min_now').val())) {
            $('.min_now').remove();
        }

        filter();
        // if (brand_qt == 1) {
        //  window.location = url + params;
        // } else
        // if (brand_qt > 1) {
        //  window.location = url + params;
        // }


    });

    $('form.all-filters.other input:checkbox').click(function() {

        if (max_price == parseInt($('.max_now').val())) {
            $('.max_now').remove();
        }

        if (min_price == parseInt($('.min_now').val())) {
            $('.min_now').remove();
        }

        filter();

    });

    $('form.all-filters.other').submit(function(e) {
        e.preventDefault();

        $('form.all-filters.other input:submit').remove();

        filter();
    });

    $('#sign .sign_button').click(function(e) {
        // e.preventDefault()
        var login = $('#sign [name="login"]').val();
        var password = $('#sign [name="password"]').val();

        $.ajax({
            url: '/accounts/login/?next=/get_user_ajax/',
            data: {
                'login': login,
                'password': password,
            },
            // data: $('.enter').serialize(),
            success: function(success) {

                $.get('/get_user_ajax/', function(newsuccess) {
                    if (parseInt(newsuccess.id) > 0) {
                        // console.log('success');
                        location.reload();
                    } else {

                        $('.enter .error').removeClass('hidden');

                    }

                }, 'JSON');
            },

            type: 'POST',
            error: function() {

                $('.enter .error').removeClass('hidden');

            }
        });
    });

    $('.step1_next').click(function(e) {
        // e.preventDefault();

        if (!$('#id_phone').val()) {
            $('#id_phone').addClass('error');
            return false;
        } else {
            $('#id_phone').removeClass('error');
        }
        $('.checkout_step-one').addClass('hidden');
        $('.step1').addClass('ready-step');
        $('.step1_now').addClass('hidden');
        $('.step1_completed').removeClass('hidden');
        $('.step2').removeClass('hidden');
        $('.checkout_order-buy').removeClass('hidden');
    });

    $('.checkout_edit-step_lnk').click(function() {

        $('.checkout_step-one').removeClass('hidden');
        $('.step1').removeClass('ready-step');
        $('.step1_now').removeClass('hidden');
        $('.step1_completed').addClass('hidden');
        $('.step2').addClass('hidden');
        $('.checkout_order-buy').addClass('hidden');
    });

    $('input[name="delivery"]').click(function() {
        var id = parseInt($(this).val());
        if (id == 1) {
            $('.samovyvoz').removeClass('hidden');
            $('.delivery-address, .delivery-service').addClass('hidden');
        }

        if (id == 2) {
            $('.delivery-address').removeClass('hidden');
            $('.samovyvoz, .delivery-service').addClass('hidden');

        }

        if (id == 3) {
            $('.delivery-service').removeClass('hidden');
            $('.delivery-address, .samovyvoz').addClass('hidden');
        }
    });

    $('.checkout_order-buy').click(function() {
        $('.enter').remove();
        $('.checkout-form').submit();
        // setTimeout(window.location.replace("/checkout/thanx/"), 3000)
    });

    $('select.dop').change(function() {
        // console.log("we are here");
        var price = $(this).find('option[value="' + $(this).val() + '"]').data('price');
        // console.log(price);
        $(this).closest('.good-service').find('.adddop span').html(price);

    });
    $('.adddop').click(function() {
        var id = $(this).closest('.good-service').find('select.dop').val();
        addToCart(id);
        // console.log(id);
    });


    $('body').on('click','.filter-mm-btns .btn-buy', function(){
        // alert('1234567890');
        var items = [];
        $('#sidebarFilter input:checked').each(function(){
            items.push($(this).attr('name') + "=1");
        })

        npath = items.join('&');
        // console.log(npath);
        window.location = window.location.pathname + "?" + npath;


    });

});
