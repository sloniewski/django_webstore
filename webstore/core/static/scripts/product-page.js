$( document ).ready( function(){

	$('#add-item-form').on('submit', function(event) {
		event.preventDefault();
		$('#cart-item-count').text(function(event){
			var form_action_url = $('#add-item-form').attr('action');
			var item_num = $('#product-id').val();
			var item_qty = $('#item-quantity').val();
			$.ajax({
				url: form_action_url,
				method: 'POST',
				data: {
					item: item_num,
					qty: item_qty
				}
			}).done(function (data) {
				data = JSON.parse(data);
				$('#cart-item-count').text(data.cart_items);
			}).fail(function() {
				return 0;
			});
		});
	});
});
