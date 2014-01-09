$(document).ready(function() {

	$('.uuidElement').first().addClass('active');
	
	var currentActiveEnt = $('.uuidElement').find('active');
	
	//loadContentDetails("No host selected");
	
	$('.uuidElement').click(function() {
		
		console.log("List element clicked");
		
		var newUUID = $(this).children("p").first().text();
		
		console.log("Found new UUID: ",newUUID);
		
		//loadContentDetails(newUUID);
	});
	
	function loadContentDetails(ident){
		
		
		
		console.log("Called loadContentDetails function");
		
		var contentArea = $(document).find('.content-details');
		
		console.log("Defined contentArea: ",contentArea);
		
		contentArea.html("<li>{{ entity.name }}</li>");
		
		
	};
});

