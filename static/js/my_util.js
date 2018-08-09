$(document).ready(function() {
	$("form").submit(function(event) {
	  event.preventDefault(); // prevent submit button from default post
	  try {
		$.post( $(location).attr('href') + "action/", // post url
				$(this).serialize(),                  // post data
				function(data,status) {               // process the post response
				  localStorage.setItem( $(location).attr('pathname').replace(/\//g, '') + "result",
										JSON.stringify(data));
				  display_summary();	// Note: this function will be customized in each page
				});
	  } catch(err) {
		alert(err);
	  }
	});
});