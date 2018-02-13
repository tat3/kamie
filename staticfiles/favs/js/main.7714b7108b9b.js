$(window).on('load', function(){
 setTimeout(function(){
     $('.js-grid').masonry({
         columnWidth: 160,
         fitWidth: true,
     });
 }, 500);
});

$(function(){
    const toggleOpacity = function(){
        let opacity = $(this).css('opacity');
        if(opacity >= 0.5){
            opacity = 0;
        }else{
            opacity = 1;
        }
        $(this).css('opacity', opacity);
    };
    const hideDOM = function(){
        $(this).css('opacity', 0);
    };
    const showDOM = function(){
        $(this).css('opacity', 1);
    };


    $('.widget_text').on({
        'click': toggleOpacity,
        'mouseover': showDOM,
        'mouseout': hideDOM
    });
});
