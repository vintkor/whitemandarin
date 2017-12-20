function getStatus(){
    var status = _.template($('#status').html());

    $.get('/hot/showstatus/', function(item){
        $('.status').html('Осталось: ' + item)
        // $('.status').html();
    }, 'JSON');
}

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
    $('body').on('click','.jstree-node', function(e){
      var id = $(this).attr('id'),
          template = _.template($('#hotline').html());

      $('input[name="id"]').val(id);
      e.stopPropagation();

      $.post('/hot/get_category_data_remote/', {id: id}, function(item){
        $('.work-area').empty();
        $('.work-area').html(template(item));

        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()

        // alert(item);
      }, 'JSON');
    });

    $('body').on('click','.savecat', function(e){
          var id = $('input[name="id"]').val(),
          data = $('.hotline').serialize();

          // console.log(data);

          $.post('/hot/savecat/' + id + '/', data, function(item){

            $('#' + id).click();
            // $('.work-area').html('<h1>' + item.name + '</h1>');
            // $('h1').after()

            // alert(item);
          }, 'JSON');
    });

    $('body').on('click', '.show-concurents', function(e){
      var id = $(this).data('id');
      $('tr#' + id).toggleClass('hidden');
      // alert(id);
    });
    $('body').on('click', '.getprice', function(e){
      var cat = $('h1').html(),
          csv = "",
          id = $('input[name="id"]').val();
      $('table.maintable > tbody > tr').each(function(){
        var product_name = $(this).find('.name').html(),
        product_price = $(this).find('.price').val();

        if (product_name){
          csv += cat + ";" + product_name.trim() + ";" + product_price.replace('.',',') + "\n";
        }

      });

      $.get('/hot/get_not_active/' + id + '/', function(items){
          _.each(items, function(item){
            csv += cat + ";" + item + ";0\n";
          });

          $('#myModal').modal('show');
          $('#myModal #csv').val(csv);
      }, 'JSON');
      // console.log(csv);
      // $('tr#' + id).toggleClass('hidden');
      // alert(id);
    });


    $('.scan-it').click(function(){
      var id = $('input[name="id"]').val();
      $.post('/hot/scan_it/', {id: id}, function(item){

        $('#' + id).click();
        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()
        getStatus();

        // alert(item);
      }, 'JSON');


    });

    $('.scan-it-remote').click(function(){
      var id = $('input[name="id"]').val();
      $.post('/hot/scan_it_remote/', {id: id}, function(item){

        $('#' + id).click();
        // $('.work-area').html('<h1>' + item.name + '</h1>');
        // $('h1').after()
        getStatus();

        // alert(item);
      }, 'JSON');
    });

    setInterval(function(){
      getStatus();
    }, 10000);


    $('body').on('change', '#selectall', function(){

      var check = $(this).is(':checked');

      $('td.check input').prop('checked', check);

      console.log(check);


      // $('#myModal').modal();
    });

    $('body').on('change', '#selectfirm', function(){

      var concurent = $(this).val();

      $('td.check input').prop('checked', false);

      $('tr[data-concurent="' + concurent + '"]').each(function(){

        var id = $(this).parent().closest('tr').attr('id');

        $('tr[data-parent="' + id + '"]').find('td.check input').prop('checked', true);
        // console.log($(this).html());
        // $(this).parent().closest('tr').find("td.check input").prop('checked', true);

        // console.log();
      });

      $('#checkfirm').val(concurent);
      // console.log(concurent);

    });

    $('body').on('click', '.changeprice', function(){

      var concurent = $('#checkfirm').val(),
          priceplus = $('.priceplus').val(),
          oper = parseInt($('#oper').val()),
          newprice = 0;

      $('tr[data-concurent="' + concurent + '"]').each(function(){

        var id = $(this).parent().closest('tr').attr('id'),
            price = $(this).data('price');

        if (oper){
          newprice = parseInt(price)+parseInt(priceplus);
        } else {
          newprice = parseInt(price)-parseInt(priceplus);
        }

        $('tr[data-parent="' + id + '"]').find('input[type="text"]').val(newprice);
        // console.log($(this).html());
        // $(this).parent().closest('tr').find("td.check input").prop('checked', true);

        console.log(newprice);
      });

      $('#checkfirm').val(concurent);
      // console.log(concurent);

    });
});
