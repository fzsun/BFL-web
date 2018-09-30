// listen on form submit and reset
$(document).ready(function () {
  $("form").on("submit", function (event) {
    event.preventDefault(); // prevent submit button from default post
    try {
      $.post($(location).attr('href') + "action/", // post url
        $(this).serialize(), // post data
        function (data, status) { // process the post response
          localStorage.setItem($(location).attr('pathname').replace(/\//g, '') + "result",
            JSON.stringify(data));
          if (typeof display_summary === 'function') {
            display_summary(); // Note: this function will be customized in each page
          }
        });
    } catch (err) {
      alert(err);
    }
  });
  $("form").on("reset", function (event) {
    try {
      localStorage.removeItem($(location).attr('pathname').replace(/\//g, '') + "result")
      if (typeof display_summary === 'function') {
        display_summary(); // Note: this function will be customized in each page
      }
    } catch (err) {
      alert(err);
    }
  });
});