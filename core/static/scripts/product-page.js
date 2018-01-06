$( document ).ready( function(){

	var csrftoken = getCookie('csrftoken');

	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});

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
				consoe.log(data);
				return item_qty;
			}).fail(function() {
				return 0;
			});
		});
	});
});