$(document).ready(function(){

    $('.buy-button').on('click',function(){
        var product_id = $(this).attr('product_id');
            req = $.ajax({
                url: '/buy',    
                type: 'POST',
                data: { product : product_id}
            });

      });

     
});
