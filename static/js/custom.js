<script>
	$(function() {
		while( $('#fitin div').height() > $('#fitin').height() ) {
			$('#fitin div').css('font-size', (parseInt($('#fitin div').css('font-size')) - 1) + "px" );
		}
	});
	
</script>