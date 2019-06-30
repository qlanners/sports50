// function that changes the displayed statistic type chosen at the top of page when a button is clicked
$('#field_tabs a').click(function (e) {
e.preventDefault();

var url = $(this).attr("data-url");
var href = this.hash;
var pane = $(this);

// Load the correct url
$(href).load(url)
});