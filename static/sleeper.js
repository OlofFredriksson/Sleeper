$(document).ready(function () {
	function refreshPage() {
		$.ajax({
			url: "/getSleepValue",
			cache: false,
			beforeSend: function() {
				$('#secondsFromFile').append("<img src='static/loading.gif' />");
			},
			success: function(data) {
				$('#secondsFromFile').html(data);
			},
			complete: function() {
				window.setTimeout(refreshPage, 1000);
			}
		});
	}
	refreshPage();
});