// using jQuery
function csrfAuth() {
	var my = this;

	my.getCookie = function(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	};

	my.csrfSafeMethod = function(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};

	my.ajaxRequest = function(url, options) {
		var csrftoken = my.getCookie('csrftoken');
		var defaults = {
			type : 'POST',
			dataType : 'json',
			crossDomain : false, // obviates need for sameOrigin test
			beforeSend : function(xhr, settings) {
				if (!my.csrfSafeMethod(settings.type)) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		}
		var settings = $.extend({}, defaults, options);
		$.ajax(url, settings);
	};
};

$(document).ready(function() {
	$('a.logout').hide();
	
	$('form:eq(1) input[type="button"]').bind('click', function() {
		var csrfObj = new csrfAuth();
		var url = 'tasks/login/';
		var data = $('form:eq(1)').serialize();

		csrfObj.ajaxRequest(url, {
			'data' : data,
			'success' : function(response) {
				if (response.result == 'success') {
					$('a.logout').show();
					alert("the user name is '" + response.data.u_name + "'");
				} else if (response.result == 'fail') {
					$('a.logout').show();
					alert("You already logged in, sir!");
				} else
					alert('can\'t find this user!');
			},
			'error' : function(xhr, textStatus, thrownError) {
				alert(xhr.statusText);
				alert(xhr.responseText);
				//alert(xhr.status);
				//alert(thrownError);
			}
		});
		return false;
	});
}); 