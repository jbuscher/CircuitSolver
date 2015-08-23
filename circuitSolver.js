(function() {
	"use strict";

	$(document).ready(function() {
		$( "#GO" ).click(function() {
			$.ajax({
				type: "POST",
				url: "helloWebApp.py",
				data: { param: $( "#input" ).val},
				success: function(data, status, JQxhr) {
					alert(data);
				},
				error: function() {
					alert("Error");
				}
			})
		})
	});
})();
	