$( document ).ready( function(){
	$('#add-item-form').on('submit', function(event) {
		event.preventDefault();
		$('#cart-item-count').text(function(event){
			return $('#item-quantity').val();
		});
	});
});