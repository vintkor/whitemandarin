

function open_reviews() {
    $('#good-rev-tab').tab('show');
}

function send_review()
{
    var paket = jQuery("input[name='paket']").val()
    if(!paket){ alert("Пропущен пакет"); return false; }
    var item_model = jQuery("input[name='item_model']").val()
    if(!item_model){ alert("Пропущена модель"); return false; }
    var item_id = jQuery("input[name='item_id']").val()
    if(!item_id){ alert("Пропущен id"); return false; }
    var p = jQuery("input[name='path']").val()
    if(!p){ alert("Пропущен путь"); return false; }

    var name = jQuery("input[name='review_name']").val()
    if(!name || parseInt(name.length) < 3)
    { 
        jQuery("input[name='review_name']").css("border","1px solid red");
        return false; 
     }
     else
     {
        jQuery("input[name='review_name']").css("border","1px solid silver");
     }
     var text = jQuery("textarea[name='review_text']").val()
    if(!text || parseInt(text.length) < 3)
    { 
        jQuery("textarea[name='review_text']").css("border","1px solid red");
        return false; 
     }
     else
     {
        jQuery("textarea[name='review_text']").css("border","1px solid silver");
     }

     var vote = jQuery("input[name='reit_review']").val()
     if(!vote)
     {
        vote = 0;
     }

     jQuery.ajax({
        url: p + '?id='+Math.random(),
        type:'post',
        dataType:'html',
        data: {'paket':paket, 'item_model':item_model, 'vote':vote, 'item_id':item_id, 'name':name, 'text':text},
        success: function(data)
        {
            alert("Благодарим за Ваш отзыв");
            jQuery("input[name='review_name']").val("");
            jQuery("textarea[name='review_text']").val("");
        }
     })


    
}
function send_answer(id)
{
    var paket = jQuery("input[name='paket']").val()
    if(!paket){ alert("Пропущен пакет"); return false; }
    var item_model = jQuery("input[name='item_model']").val()
    if(!item_model){ alert("Пропущена модель"); return false; }
    var item_id = jQuery("input[name='item_id']").val()
    if(!item_id){ alert("Пропущен id"); return false; }
    var p = jQuery("input[name='path_answer']").val()
    if(!p){ alert("Пропущен путь"); return false; }

    var name = jQuery("input[name='review_name_"+id+"']").val()
    if(!name || parseInt(name.length) < 3)
    { 
        jQuery("input[name='review_name_"+id+"']").css("border","1px solid red");
        return false; 
     }
     else
     {
        jQuery("input[name='review_name_"+id+"']").css("border","1px solid silver");
     }
     var text = jQuery("textarea[name='review_text_"+id+"']").val()
    if(!text || parseInt(text.length) < 3)
    { 
        jQuery("textarea[name='review_text_"+id+"']").css("border","1px solid red");
        return false; 
     }
     else
     {
        jQuery("textarea[name='review_text_"+id+"']").css("border","1px solid silver");
     }

     

     jQuery.ajax({
        url: p + '?id='+Math.random(),
        type:'post',
        dataType:'html',
        data: {'paket':paket, 'item_model':item_model, 'id':id, 'item_id':item_id, 'name':name, 'text':text},
        success: function(data)
        {
            alert("Благодарим за Ваш отзыв");
            jQuery("input[name='review_name_"+id+"']").val("");
            jQuery("textarea[name='review_text_"+id+"']").val("");
            jQuery("#ansver_"+id).hide('500');
        }
     })


    
}

function send_utility(id, positive)
{
    var p = jQuery("input[name='path_utility']").val()
    if(!p){ alert("Пропущен путь"); return false; }
    jQuery("#reit_comment_"+id).html("Благодарим, Ваша оценка учтена");
    jQuery.ajax({
        url: p + '?id='+Math.random(),
        type:'post',
        dataType:'html',
        data: {'id':id, 'positive':positive},
        success: function(data)
        {
            
            jQuery("#reit_comment_"+id).html("<span class='red'>Благодарим, Ваша оценка учтена</span>");
        }
     })

}