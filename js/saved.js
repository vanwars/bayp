// $('#myModal').modal(options);

$('li.success').hide();

$('li.bookmark').click(function(){
	if($(this).children('a').hasClass('success')) {
		console.log('he');
	}
	else {
		$(this).next().fadeIn(1000).fadeOut(1000);	
	}
	$(this).children('a').toggleClass('success')
});