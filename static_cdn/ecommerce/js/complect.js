$(document).ready(function(){
    $('#tree').jstree({
    'core' : {
      'data' : {
        'url' : '/hot/get_category/',
        'data' : function (node) {
          return { 'id' : node.id };
        }
      }
    }

  });

    $('body').on('click','.delete', function(e){
      var id = $(this).parent().data('id');

      $.post('/deletecomplect/', {id:id}, function(success){
        // alert(id);

      });

      $(this).parent().remove();



    });
    $('body').on('click','.jstree-node', function(e){
      var id = $(this).attr('id');
          template = _.template($('#one').html()),
          ctemplate = _.template($('#complect').html());
          selectbrand = "";

      $('input[name="maincat"]').val(id);
      e.stopPropagation();

      $.post('/getcatcomplect/', {id: id}, function(success){
        $('.items').empty();
        _.each(success.items, function(item){

          $('.items').append(template(item));
        });

        _.each(success.complects, function(item){

          $('.citems').append(ctemplate(item));
        });

        _.each(success.brands, function(item){

          selectbrand += "<option value='" + item.value + "'>" + item.name + "</option>";

        });
        $('select.brands').empty();
        $('select.brands').append(selectbrand);

        $('.second').removeClass('hidden');

        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()

        // alert(item);
      }, 'JSON');
    });

    $.post('/getcattree/', function(items){

        var selectcat = ""

        _.each(items, function(item){

           selectcat += "<option value='" + item.value + "'>" + item.name + "</option>";

        });

        $('select.categories').append(selectcat);

    });

    $('select.brands').change(function(){
      alert($(this).val());
    });

    $('select.categories').change(function(){
      var id = $(this).val(),
          template = _.template($('#one').html());

      $.post('/getcatcomplect/', {id: id}, function(success){
        $('.complect_items').empty();
        _.each(success.items, function(item){

          $('.complect_items').append(template(item));
        });
        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()

        // alert(item);
      }, 'JSON');
    });

    $('.maincat-form').submit(function(e){
      e.preventDefault();

      $.post('/createcomplect/', $(this).serialize(), function(){
        alert('ok');
      });

      // alert($(this).serialize());

    })
});
