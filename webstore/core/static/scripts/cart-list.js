$(document).ready(function () {

    var plus = $('.add_one_item');
    var minus = $('.remove_one_item');
    
    function update_totals(value, qty){
        $('#cart_summary_item_count').text(qty);
        $('#cart_summary_total_value').text(value);
    }

    plus.on('click', function(event){
        event.preventDefault();
        var collection_item = $(this).parent().parent();
        var qty_box = collection_item.find('#item_qty');
        var value_box = collection_item.find('#item_value');
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            method: 'POST',
        }).done(function (data) {
            qty_box.text(data.item_qty);
            value_box.text(data.item_value);
            update_totals(data.cart_value, data.cart_items);
        }).fail(function () {
            return 0;
        });
    });

    minus.on('click', function(event) {
        event.preventDefault();
        var collection_item = $(this).parent().parent();
        var qty_box = collection_item.find('#item_qty');
        var value_box = collection_item.find('#item_value');
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            method: 'POST',
            statusCode: {
                204: function (data) {
                    collection_item.slideUp('slow', function(){
                        $(this).remove();
                    });
                    update_totals(data.cart_value, data.cart_items);
                },
                200: function (data) {
                    qty_box.text(data.item_qty);
                    value_box.text(data.item_value);
                    update_totals(data.cart_value, data.cart_items);
                }
            }
        }).fail(function () {
            return 0;
        });
    });
});