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
        'click': toggleVisible,
    });

    $('.js-fav').on({
        'click': function(){
            const self = $(this);
            const widget = $(this).parent().parent().parent();
            // Get current state
            let url = self.data('save');
            let isSaved = false;
            if(self.hasClass('js-fav-saved')){
                url = self.data('delete');
                isSaved = true;
            }
            // Switch state from save to unsaved or from unsaved to saved
            isSaved = !isSaved;
            if(isSaved){
                self.removeClass('btn-success js-fav-unsaved');
                self.addClass('btn-danger js-fav-saved');
                self.text('お気に入り解除');
                widget.addClass('js-fav-border');
            }else{
                self.removeClass('btn-danger js-fav-saved');
                self.addClass('btn-success js-fav-unsaved');
                self.text('お気に入り登録');
                widget.removeClass('js-fav-border');
            }
            // GET request to database server
            $.get(url);

        }
    });
});
