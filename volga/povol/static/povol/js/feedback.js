function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);          
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function objectifyForm(formArray) {//serialize data function

  var returnArray = {};
  for (var i = 0; i < formArray.length; i++){
    returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
}

$(document).ready(function() {	
	$( "#feedback_form" ).submit(function( event ) {		
		event.preventDefault();
		processFeedback(this);
		
	});
	        
    $('#response_message .close_btn').click(function(){
        $.fancybox.close('#response_message');
        return false;
    });

    $('#response_message .ok_btn').click(function(){
        $.fancybox.close('#response_message');
        return false;
    });
});
    
function processFeedback(self) {
	$.fancybox.close([{ "src": "#popup" }] );		
	var form = $(self);
	var url = form.data('url');
	var data = objectifyForm(form.serializeArray());
	data.csrfmiddlewaretoken = getCookie('csrftoken');                  
    $.ajax({
        url: url,
        type: "POST",                                
        data: data,
        cache: false,
        success: function(data) {        	
        	$.fancybox.open([{ "src": "#response_message", "modal": true }] );
        	if (data.status) {
        		$('#response_message .modal-content').addClass('success');        		
        		form.trigger("reset");
        	} else {
        		$('#response_message .modal-content').addClass('error');
        		$('#response_message .modal-content').html(data.errors);
        	}    
        },
        error: function (jqXHR, exception) {
        	$.fancybox.open([{ "src": "#response_message", "modal": true }] );
            $('#response_message .modal-content').addClass('error');
            var msg = '';                
            if (jqXHR.status === 0) {
                msg = 'Not connect.\n Verify Network.';
            } else if (jqXHR.status == 404) {
                msg = 'Requested page not found. [404]';
            } else if (jqXHR.status == 500) {
                msg = 'Internal Server Error [500].';
            } else if (exception === 'parsererror') {
                msg = 'Requested JSON parse failed.';
            } else if (exception === 'timeout') {
                msg = 'Time out error.';
            } else if (exception === 'abort') {
                msg = 'Ajax request aborted.';
            } else {
                msg = 'Uncaught Error.\n' + jqXHR.responseText;
            }            
            $('#response_message .modal-content').html(msg);
        },
    });
}


