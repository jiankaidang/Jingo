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