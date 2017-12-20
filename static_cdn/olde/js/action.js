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

      $.post('/setaction/', {ids:id}, function(success){
        // alert(id);

      });

      $(this).parent().remove();



    });
    $('body').on('click','.jstree-node', function(e){
      var id = $(this).attr('id');
          template = _.template($('#one').html()),
          atemplate = _.template($('#action').html());
          selectbrand = "";

      $('input[name="maincat"]').val(id);
      e.stopPropagation();

      $.get('/getactionbycat/' + id + "/", function(success){
        $('.aitems').empty();
        _.each(success.items, function(item){

          $('.items').append(template(item));
        });

        _.each(success.aitems, function(item){

          $('.aitems').append(atemplate(item));
        });

        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()

        // alert(item);
      }, 'JSON');
    });


    $('body').on('click', 'input[type="checkbox"]', function(){
      var items = [];
      $( "input:checked" ).each(function(){
        items.push($(this).data('id'));
      });

      $('input[name="ids"]').val(items.join())
      // alert(items;/..kljl;);
    })

    // $('.maincat-form').submit(function(e){
    //   e.preventDefault();

    //   $.post('/createcomplect/', $(this).serialize(), function(){
    //     alert('ok');
    //   });

    //   // alert($(this).serialize());

    // });

    $('.create').click(function(){
      var name = $('input[name="name"]').val(),
        date = $('input[name="date"]').val(),
        ids = $('input[name="ids"]').val();
      $.post('/setaction/', {name: name, date: date, ids: ids},function(){

        alert('Акции успешно созданы');

      } );
    });
});
