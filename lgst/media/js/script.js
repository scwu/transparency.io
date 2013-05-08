$(document).ready(function() {
    $("#enter-button").click(function() {
        var text = $('#search-txt').val();
        lightbox('', '/_request_data', text);
    });
    
    $(document).keypress(function(e) {
    if(e.which == 13) {
        var text = $('#search-txt').val();
        lightbox('', '/_request_data', text);
    }
    });
    
function lightbox(insertContent, ajaxContentUrl, text){

	// jQuery wrapper (optional, for compatibility only)
	(function($) {
	
		// add lightbox/shadow <div/>'s if not previously added
		if($('#lightbox').size() == 0){
			var theLightbox = $('<div id="lightbox"/>');
			var theShadow = $('<div id="lightbox-shadow"/>');
			$(theShadow).click(function(e){
				closeLightbox();
			});
			$('body').append(theShadow);
			$('body').append(theLightbox);
		}
		
		// remove any previously added content
		$('#lightbox').empty();
		
		// insert HTML content
		if(insertContent != null){
			$('#lightbox').append(insertContent);
		}
		
		// insert AJAX content
		if(ajaxContentUrl != null){
			// temporarily add a "Loading..." message in the lightbox
			$('#lightbox').append('<p class="loading">Loading...</p>');
			
			// request AJAX content
			$.ajax({
				type: 'POST',
				url: ajaxContentUrl,
                dataType: "json",
                data: {
                    'result' : text,
                },
				success:function(response){
                    var arr = new Array();
                    for (var i = 0; i < response.length; i++) {
                        var name = response[i].name;
                        var type = response[i].type;
                        var id = response[i].id;
                        if ((type === 'organization') && ($.inArray(name, arr) === -1)) {
                            upper = name.toUpperCase();
                            var html = '<a href="#" class="company-link" id ="' + response[i].id + '"><p class="company-name">' + upper + '</p></a>';
                            arr.push(html);
                        }
                    }
                    $('#lightbox').empty();
                    $('#lightbox').append('<div class="results"><p class="results">RESULTS:</p></div>');
                    for (var j = 0; j < arr.length; j++) {
                        if (j%2 == 0) {
                            $('#lightbox').append('<div class="company-name" id="light">' + arr[j] + '</div>');
                        } else {
                            $('#lightbox').append('<div class="company-name" id="dark">' + arr[j] + '</div>');
                        }
                    }
                    if (arr.length === 0) {
                      $('#lightbox').append('<div class="company-name" id="light"><p class="company-name">I\'m sorry, but there are no results available for that company.</p></div>');
                    }
                    $(".company-link").on("click", function(event){
                        event.preventDefault();
                        var company_id = this.id;
                        window.location = '/organization/' + company_id;
                        return false;
                    });
                    
				},
				error:function(){
					alert('AJAX Failure!');
				}
			});
		}
		
		// move the lightbox to the current window top + 100px
		$('#lightbox').css('top', $(window).scrollTop() + 100 + 'px');
		
		// display the lightbox
		$('#lightbox').show();
		$('#lightbox-shadow').show();
	
	})(jQuery); // end jQuery wrapper
	
}

// close the lightbox
function closeLightbox(){
	
	// jQuery wrapper (optional, for compatibility only)
	(function($) {
		
		// hide lightbox/shadow <div/>'s
		$('#lightbox').hide();
		$('#lightbox-shadow').hide();
		
		// remove contents of lightbox in case a video or other content is actively playing
		$('#lightbox').empty();
	
	})(jQuery); // end jQuery wrapper
}
});
