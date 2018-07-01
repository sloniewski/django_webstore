$(document).ready(function () {

    var plus = $('.add_one_item');
    var minus = $('.remove_one_item');

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
                },
                200: function (data) {
                    qty_box.text(data.item_qty);
                    value_box.text(data.item_value);
                }
            }
        }).fail(function () {
            return 0;
        });
    });
});