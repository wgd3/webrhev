$(document).ready(function() {

	$('.uuidElement').first().addClass('active');
	
	var currentActiveEnt = $('.uuidElement').find('active');
	
	//loadContentDetails("No host selected");
	
	$('.uuidElement').each(function() {
		
		var newUUID = $(this).find("p").text()
		console.log("Modifying href to: "+newUUID);
		var newURL = "http://localhost:5000/host/"+newUUID;
		$(this).find("a").attr('href',newURL);
		
	});
	
	$('.uuidElement').click(function() {
		
		console.log("List element clicked");
		//remove 'active' class from whatever currently has it
		$('uuidElement').find('active').toggleClass('active');
		
		// add active class to clicked element
		$(this).toggleClass('active');

		
	});
	
	$('#progressDiv').hide()

	
	function loadContentDetails(ident){
		
		// Really need to find a way to do the following:
		// get passed a uuid
		// set the content of the Host Details tab to the details of the host uuid passed
		// repopulate the error messages  table with messages from the host passed
		//
		// Maybe with cookies?
				
		console.log("Called loadContentDetails function");
		
		var contentArea = $(document).find('.content-details');
		
		console.log("Defined contentArea: ",contentArea);
		
		var newURL = "host/"+ident;
		
		console.log("Redirecting to " + newURL);
		
		window.location = newURL;
		
	};
});

