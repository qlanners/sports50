
var width = 960;
var height = 600;


var projection = d3.geoAlbersUsa()
    .scale(1250)
    .translate([width / 2, height / 2]);

var path = d3.geoPath();

var stadium_map = function(stadiums, s) {

    var svg3 = d3.select("#third_svg")
    var div = d3.select("#third_svg_tooltip")
    svg3.selectAll("circle").remove();
    
    svg3.selectAll("dot")
      .data(stadiums)
      .enter()
      .append("circle")
      .attr("class", "stadiums")
      .attr("cx",function(d){return projection([d[3], d[4]])[0]})
      .attr("cy",function(d){return projection([d[3], d[4]])[1]})
      .attr("r", function(d){if (d[7]>=1){ return ((Math.log(d[7]+3))**2) } else { return 0 }}) 
      .attr("opacity",0.9)
      .style("fill", function(d){if (d[5]==1) { return "gold" } else { return "blue"}})
          .on("mouseover", function(d) {  
            var stat_name = s.options[s.selectedIndex].text;
              div.transition()    
                  .duration(200)    
                  .style("opacity", .9);    
              div.html(function(){if (stat_name=='% Complete') {
                return d[2] + "<br/>" + "-" + "<br/>" + d[1] + "," + d[0] + "<br/>" + "(" + d[7].toFixed(2) +stat_name+")"}
                else {
                  return d[2] + "<br/>" + "-" + "<br/>" + d[1] + "," + d[0] + "<br/>" + "(" + d[7] + " "+stat_name+")"
                }})
                  .style("left", (d3.event.pageX) + "px")   
                  .style("top", (d3.event.pageY - 28) + "px");  
              })          
          .on("mouseout", function(d) {   
              div.transition()    
                  .duration(500)    
                  .style("opacity", 0); 
        });             
}

// function create_map(stadiums){
//   var svg3 = d3.select("#svg3").append("svg").attr("width", "960").attr("height", "600").attr("id", "third_svg");

//   var div = d3.select("body").append("div")
//       .attr("class", "tooltip").attr("id","third_svg_tooltip")      
//       .style("opacity", 0); 

//   svg3.append("rect").attr("height",height).attr("width",width).attr("fill","white").attr("opacity",0)   

//   d3.json("https://d3js.org/us-10m.v1.json", function(error, us) {
//     if (error) throw error;

//     svg3.append("g")
//         .attr("class", "states")
//       .selectAll("path")
//       .data(topojson.feature(us, us.objects.states).features)
//       .enter().append("path")
//         .attr("d", path);

//     svg3.append("path")
//         .attr("class", "state-borders")
//         .attr("d", path(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; })));

//       var s = document.getElementById("stats_choice");
//         var stats_choice = s.options[s.selectedIndex].value;      
//       for (var j = 0; j < stadiums.length; j++) {
//         var this_stad =0
//       for(var i = 2010; i < 2018; i++) { this_stad = this_stad + stadiums[j][6][stats_choice][i];};
//     stadiums[j].push(this_stad) }
//     stadium_map(stadiums, s)        

//    });
//   return svg3;
// };

function update(){
  var s = document.getElementById("stats_choice");
  var stats_choice = s.options[s.selectedIndex].value;
  var seasons = [];
  d3.selectAll(".myCheckbox").each(function(d){
    cb = d3.select(this);
    if(cb.property("checked")){
      seasons.push(cb.property("value"));
    }
  });
  var arrayLength = seasons.length
  while (stadiums[0].length > 7){
    for(var t = 0; t < stadiums.length; t++) {
      stadiums[t].pop()
    }
  }

  for (var j = 0; j < stadiums.length; j++) {
    var this_stad =0
    var seasons_played_here = 0
    for(var i = 0; i < arrayLength; i++) { if (stadiums[j][6][stats_choice][seasons[i]]>0) {
      this_stad = this_stad + stadiums[j][6][stats_choice][seasons[i]];
      seasons_played_here = seasons_played_here + 1;}
    }
if (stats_choice == 'percentage__sum'){
stadiums[j].push((this_stad/seasons_played_here)*100)}
else {
stadiums[j].push(this_stad)
}
  }     

  stadium_map(stadiums, s)

}