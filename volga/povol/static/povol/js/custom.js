$(document).ready(function() {
    $('.main_nav_menu').singlePageNav({
        speed: 600
    });
    setTimeout(function() {
        $('body').addClass('loaded');
    }, 100);
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

    $(window).scroll(function () {
        if (($(this).scrollTop() > $('.main_header').height()) && ($(this).scrollTop() < ($(document).height() - $('.schedule_about').height()))) {
            $('.side_btn').addClass('active');            
        }
        else {
            $('.side_btn').removeClass('active'); 
        }
    });
});

$(function () {
    $.scrollUp({
        scrollDistance: 400,          // Distance from top/bottom before showing element (px)
        scrollFrom: 'top',            // 'top' or 'bottom'
        scrollSpeed: 600,             // Speed back to top (ms)
        easingType: 'easeOutCubic',   // Scroll to top easing (see http://easings.net/)
        animationSpeed: 200,          // Animation in speed (ms)
        scrollText: '',               // Text for element, can contain HTML
        scrollTitle: 'Наверх',        // Set a custom <a> title if required. Defaults to scrollText
        scrollImg: false,             // Set true to use image
        zIndex: 850                   // Z-Index for the overlay
    });
});

$('#price_tabs').tabs();