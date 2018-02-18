/*$(window).on('load', function(){
 setTimeout(function(){
     $('.js-grid').masonry({
         columnWidth: 160,
         fitWidth: true,
     });
 }, 500);
});*/

$(window).ready(function(){
    const wrap = $('.js-grid');
    const backyard = $('js-grid-backyard');
    wrap.masonry({
         columnWidth: 320,
         fitWidth: true,
     });
    $('.js-grid-img').each(function(index, elm){
        elm.onload = function(){
            const item = $(this).parent().parent();
            wrap.append(item);
            // wrap.masonry('reloadItems').masonry('layout');
            wrap.masonry('appended', item).masonry();
        };
        elm.src = $(elm).data('url');
    });
});

$(function(){
    const hide_object = function(){
        $(this).removeClass('show');
    };
    const show_object = function(){
        $(this).addClass('show');
    };
    const toggleVisible = function(){
        if($(this).hasClass('show')){
            hide_object.call(this);
        }else{
            show_object.call(this);
        }
    };

    $('.widget_text.pc').on({
        'mouseover': show_object,
        'mouseout': hide_object,
        'click': toggleVisible,
    });

    $('.widget_text.sp').on({
        //'mouseover': show_object,
        //'mouseout': hide_object,
        'click': toggleVisible,
    });
});
