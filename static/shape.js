

var svg = d3.select("body").append("svg").attr("height","100%").attr("width","100%");


svg.selectAll("rect").data(touchdowns).enter().append("rect");