// Create a jquery function to navigate to new graphic when a new tab is pushed
$('#myTabs a').click(function (e) {
	e.preventDefault();
  
	var url = $(this).attr("data-url");
  var href = this.hash;
  var pane = $(this);
	
	$(href).load(url)
});

// When the page is loaded ("DOMContentLoaded"), then click the first tab to display the graphic upon load
document.addEventListener("DOMContentLoaded", function(event) { 
  document.getElementById("field_button").click();
});