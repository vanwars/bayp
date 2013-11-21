// $(document).ready(function() {
// 	var $main_toggle = $('button.navbar-toggle.main-toggle');
// 	// var $account_toggle = $('.account-toggle');
	
// 	$('.account-toggle').on('click', function() {
// 		var $main_has_collapsed = $main_toggle.hasClass('collapsed');
// 		console.log($main_has_collapsed);
// 		if ($main_has_collapsed == false) {
// 			console.log($('.bs-js-navbar-collapse'));
// 			$('').addClass('in');
// 		}
// 	});
// });


$(document).ready(function() {
	var $account_target = $($('button.navbar-toggle.account-toggle').data('target'));
	var $main_target = $($('button.navbar-toggle.main-toggle').data('target'));

	console.log($account_target);

});