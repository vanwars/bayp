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
	var $list_text = $(this).nextAll('small').children('span');
	var $list_num = parseInt($list_text.text());

	if($(this).children('span').hasClass('success')) {
		$list_num -= 1;
		$list_text.text($list_num);
		console.log('yes');
	}
	else {
		$list_num += 1;
		$list_text.text($list_num);
		$(this).nextAll('.success').fadeIn(1000).fadeOut(1000);	
	}
	$(this).children('span').toggleClass('success');
});

$('a.single-rec').click(function(e){
	e.preventDefault();
	var $single_text = $(this).nextAll('strong').children('');
	var $single_num = parseInt($single_text.text());
	console.log($single_num);
	if($(this).children('span').hasClass('success')) {
		$single_num -= 1;
		$single_text.text($single_num);
		console.log('yes');
	}
	else {
		$single_num += 1;
		$single_text.text($single_num);
		$(this).nextAll('.success').fadeIn(1000).fadeOut(1000);	
	}
	$(this).children('span').toggleClass('success');
});

$('a.single-save').click(function(){
	$(this).toggleClass('btn-success');	
	if($(this).hasClass('btn-success')) {
		$(this).children('strong').text(" Saved Program");
	}
	else {
		$(this).children('strong').text(" Save Program");
	}
	
	
});

$('#myModal').modal(options);