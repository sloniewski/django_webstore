$( document ).ready( function(){

    $('.quick-add-item').on('click', function(event) {
		event.preventDefault();
        url = $(this).attr('href');
		$.ajax({
			url: url,
			method: 'POST',
		}).done(function (data) {
            $('#cart_item_count').html(data.cart_items);
		}).fail(function() {
			return 0;
		});
    });

});
