$(document).ready(function() {

    $('.slider-mp').owlCarousel({
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false
            },
            600: {
                items: 1,
                nav: false
            },
            1000: {
                items: 1,
                nav: false,
                loop: true
            }
        }
    });
    $('.goods-carousel').owlCarousel({
        loop: true,
        margin: 10,
        responsiveClass: true,
        navText: ['<i class="fa fa-long-arrow-left" aria-hidden="true"></i>', '<i class="fa fa-long-arrow-right" aria-hidden="true"></i>'],
        responsive: {
            0: {
                items: 2,
                nav: false,
                dots: true
            }
            ,
            400: {
                items: 3,
                nav: false,
                dots: true
            },
            600: {
                items: 4,
                nav: false,
                dots: true
            },
            1000: {
                items: 5,
                dots: false,
                nav: true
            },
            1200: {
                items: 6,
                dots: false,
                nav: true
            }
        }
    });
    $('.good-packages').owlCarousel({
        loop: true,
        autoplay: true,
        margin: 10,
        responsiveClass: true,
        navText: ['<i class="fa fa-long-arrow-left" aria-hidden="true"></i>', '<i class="fa fa-long-arrow-right" aria-hidden="true"></i>'],
        responsive: {
            0: {
                items: 1,
                nav: false,
                dots: true
            },
            600: {
                items: 1,
                nav: false,
                dots: true
            },
            1000: {
                items: 1,
                nav: true,
                dots: false
            }
        }
    });
    $(function() {
        $('[data-toggle="tooltip"]').tooltip()
    })
    $(function() {
        if ($("#filterPrice").length) {
            $("#filterPrice").slider({
                range: true,
                min: 0,
                max: 500
            });
        }
    });
    $("#sidebarMenu").mmenu({
        extensions: [
            "pagedim-black",
            "theme-white",
            "multiline",
            "border-full"
        ],
        offCanvas: {
            zposition: "front",
            pageSelector: "#wrapper"
        },
        navbar: {
            title: "Меню"
        },
        navbars: [{
            position: 'top',
            content: [
                '<a href="/" class="sidebar-mm-logo"><span class="sidebar-mm-logo--20">20</span><span class="sidebar-mm-logo--k">K</span></a>'
            ]
        }, {
            position: 'top',
            content: [
                'prev',
                'title'
            ]
        }]
    });
    $("#sidebarFilter").mmenu({
        extensions: [
            "pagedim-black",
            "theme-white",
            "border-full"
        ],
        offCanvas: {
            zposition: "front",
            pageSelector: "#wrapper",
            position: "right"
        },
        navbar: {
            title: "Подбор параметров"
        },
        navbars: [{
            position: 'top',
            content: [
                'prev',
                'title'
            ]
        }, {
            position: 'bottom',
            content: [
                '<span class="filter-mm-btns"><button class="btn btn-sm btn-success btn-block btn-buy">Применить</button></span>', '<span class="filter-mm-btns"><button class="btn btn-sm btn-default btn-block btn-cancel-f-mm">Отмена</button></span>'
            ]
        }]
    });
    var API = $("#sidebarFilter").data("mmenu");

    $(".btn-cancel-f-mm").click(function() {
        API.close();
    });
});

jQuery(document).ready(function($) {
    // browser window scroll (in pixels) after which the "back to top" link is shown
    var offset = 300,
        //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
        offset_opacity = 1200,
        //duration of the top scrolling animation (in ms)
        scroll_top_duration = 700,
        //grab the "back to top" link
        $back_to_top = $('.cd-top');

    //hide or show the "back to top" link
    $(window).scroll(function() {
        ($(this).scrollTop() > offset) ? $back_to_top.addClass('cd-is-visible'): $back_to_top.removeClass('cd-is-visible cd-fade-out');
        if ($(this).scrollTop() > offset_opacity) {
            $back_to_top.addClass('cd-fade-out');
        }
    });

    //smooth scroll to top
    $back_to_top.on('click', function(event) {
        event.preventDefault();
        $('body,html').animate({
            scrollTop: 0,
        }, scroll_top_duration);
    });
});