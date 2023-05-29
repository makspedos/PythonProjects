$(document).ready(function() {
    var form = $('#form_buying_product');
    console.log(form);


        function basketUpdating(product_id , number, is_delete){
            var data = { };
            data.product_id = product_id;
            data.number = number;

            var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;


            if (is_delete){
                data["is_delete"] = true;
            }
            var url= form.attr("action")

            console.log(data)
            $.ajax({
                url: url,
                type: 'POST',
                data:data,
                cache: true,
                success: function (data){
                    console.log("OK");
                    console.log(data.products_total_count)
                    if (data.products_total_count || data.products_total_count ==0 ){
                        $('#basket_total_count').text("(" + data.products_total_count + ")" )
                        console.log(data.products)
                        $('.navbar-basket ul').html("");
                        $.each(data.products, function(k, v){
                            $('.navbar-basket ul').append('<li>'+ v.product_name +',\n' + v.count + ' кількість\n,'
                                + v.total_price +'  грн ' +
                            '<a class="delete-item"  href="" data-product_id="' + v.id+ '">X</a>'+ '</li>');
                        })
                    }
                },
                error: function (){
                    console.log("ERROR")
                }
            })
        }


        form.on('submit', function (e) {
            e.preventDefault();
            var number = $('#num').val();
            console.log(number);
            var submit_data_btn = $('#submit-btn');
            var product_id = submit_data_btn.data("product_id");
            var product_name = submit_data_btn.data("product_name");
            var product_price = submit_data_btn.data("product_price");
            var total_price = number * product_price

            basketUpdating(product_id, number, false)
    });
    function refreshPage(){
    window.location.reload();
}

    function showingBasket(){
        $('.navbar-basket').removeClass('hidden');
    };

    function unshowingBasket(){
        $('.navbar-basket').addClass('hidden');
    };
    var basketVisible = false;

    $('.basket-container').click(function(){
      if (basketVisible) {
        unshowingBasket();
      } else {
        showingBasket();
      }

      basketVisible = !basketVisible;
    });


    $(document).on('click', '.delete-item', function (e){
        e.preventDefault()
        product_id = $(this).data("product_id")
        number = 0
        basketUpdating(product_id, number, true)
    });

    function calculatingPriceInBasket(){
        var total_order_amount = 0
        $('.total_product_in_basket_amount').each(function (){
            total_order_amount += parseFloat ($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2))
    };
    $(document).on('change', '.product-in-basket-amount', function (){
        var current_amount = $(this).val()
        var current_tr = $(this).closest('tr')
        var current_price_for_product = parseFloat(current_tr.find('.product-in-basket-price').text()).toFixed(2);
        var total_price = parseFloat(current_price_for_product*current_amount).toFixed(2)
        current_tr.find('.total_product_in_basket_amount').text(total_price)

        calculatingPriceInBasket()
    });

    calculatingPriceInBasket()
});