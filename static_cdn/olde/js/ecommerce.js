$(document).ready(function(){
    $('#tree').jstree({
    'core' : {
      'data' : {
        'url' : '/get_nodes/',
        'data' : function (node) {
          return { 'id' : node.id };
        }
      }
    }

  });

    $('.importcsv').submit(function(e){
      var data = $(this).serialize(),
          id = $('input[name="url_id"]').val();
      e.preventDefault();
      $.post('/importcsv/', data, function(items){
        // alert('Добавлено: ' + items.length);

        $('#myModal').modal('hide');
        $('#' + id).click();

      });

    });

    $('body').on('click','.jstree-node', function(e){
      var id = $(this).attr('id'),
          template = _.template($('#work-area').html());

      $('input[name="url_id"]').val(id);
      e.stopPropagation();

      $.post('/get_one_node/', {id: id}, function(item){
        $('.work-area').empty();
        $('.work-area').html(template(item));

        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()

        // alert(item);
      }, 'JSON');
    });

    $('.add-url-0').click(function(){
      $('input[name="url_id"]').val(0);
    });

    $('body').on('click', '.import', function(){
      $('#myModal').modal();
    });


    $('body').on('click', '.delete-phrase', function(){
      var tr = $(this).closest('tr');
      var id = tr.attr('data-id');
      $.post('/delete_phrase/', {id: id});
      tr.remove();
      alert(id);
    })
});
