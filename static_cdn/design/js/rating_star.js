(function(a){
    a.fn.webwidget_rating_sex=function(p){
        var p=p||{};

        var b=p&&p.rating_star_length?p.rating_star_length:"5";
        var c=p&&p.rating_function_name?p.rating_function_name:"";
        var e=p&&p.rating_initial_value?p.rating_initial_value:"0";
        var d="/static_cdn/design/img";
        var f=e;
        var g=a(this);
        b=parseInt(b);
        init();
        g.next("ul").children("li").hover(function(){
            jQuery(this).parent().children("li").css('background-position','0px 0px');
            var a=jQuery(this).parent().children("li").index(jQuery(this));
            jQuery(this).parent().children("li").slice(0,a+1).css('background-position','0px -28px')
            },function(){});
        g.next("ul").children("li").click(function(){
            var a=jQuery(this).parent().children("li").index(jQuery(this));
            f=a+1;
            g.val(f);
            if(c!=""){
                eval(c+"("+g.val()+")")
                }
            });
    g.next("ul").hover(function(){},function(){
        if(f==""){
            jQuery(this).children("li").slice(0,f).css('background-position','0px 0px')
            }else{
            jQuery(this).children("li").css('background-position','0px 0px');
            jQuery(this).children("li").slice(0,f).css('background-position','0px -28px')
            }
        });
function init(){
    jQuery(g).append('<div style="clear:both;"></div>')
    //jQuery('<div style="clear:both;"></div>').insertAfter(g);
    g.css("float","left");
    var a=jQuery("<ul>");
    a.addClass("webwidget_rating_sex");
    for(var i=1;i<=b;i++){
        a.append('<li style="background-image:url('+d+'/web_widget_star.png)"><span>'+i+'</span></li>')
        }
        a.insertAfter(g);
    if(e!=""){
        f=e;
        g.val(e);
        g.next("ul").children("li").slice(0,f).css('background-position','0px -28px')
        }
    }
}
})(jQuery);
