$('.success').hide();

$('li.bookmark').click(function(){
	if($(this).children('a').hasClass('success')) {
		console.log('he');
	}
	else {
		$(this).next().fadeIn(1000).fadeOut(1000);	
	}
	$(this).children('a').toggleClass('success')
});

$('a.recommend').click(function(){
	var $rec_text = $(this).nextAll('small').children('span');
	var $rec_num = parseInt($rec_text.text());
	if($(this).children('span').hasClass('success')) {
		$rec_num -= 1;
		$rec_text.text($rec_num);
		console.log('yes');
	}
	else {
		$rec_num += 1;
		$rec_text.text($rec_num);
		$(this).nextAll('a.success').fadeIn(1000).fadeOut(1000);	
	}
	$(this).children('span').toggleClass('success');
});

$('#myModal').modal(options);