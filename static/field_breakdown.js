var locationTD = function(location_td,s) {
  var svg = d3.select("#first_svg")
  var div = d3.select("#first_svg_tooltip")
  svg.selectAll("rect").remove();
  svg.selectAll("rect").data(location_td).enter().append("rect").attr("height","436")
  .attr("width","80")
  .attr("x",function(d,i){if (i<5) {return 197+(i*80)} else {return 197+(i*80)+5}}).attr("y","27").attr("fill","green").attr("opacity","0.1")
  .on("mouseover", function(d,i){ 
    d3.select(this).attr("fill","blue").attr("opacity","0.7")
    var xPosition = 40+parseFloat(d3.select(this).attr("x"))+(parseFloat(d3.select(this).attr("width"))/2)
    var yPosition = parseFloat(d3.select(this).attr("y")) + 500   
    var stat_name = s.options[s.selectedIndex].text; 
    div.transition()    
                  .duration(200)    
                  .style("opacity", .9);    
              div.html(function(){
                if (stat_name=='% Complete') {
                  return d.toFixed(2)+stat_name}
                else {
                  return d+" "+stat_name}})
                  .style("left", xPosition + "px")   
                  .style("top", yPosition + "px");  
              })      
        .on("mouseout", function(d) {  
              d3.select(this).attr("fill","green").attr("opacity","0.1") 
              div.transition()    
                  .duration(500)    
                  .style("opacity", 0); 
        });    
}

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
  var newData = [0,0,0,0,0,0,0,0,0,0]
  var arrayLength = seasons.length

  if(seasons.length > 0){
    for(var i = 0; i < arrayLength; i++) { newData = newData.map(function(num,idx){ return num + location_td[stats_choice][seasons[i]][idx];})}
  } else {
    newData = newData;  
  }            


if (stats_choice == 'percentage__sum'){
var newData = newData.map(function(element) {
return (element/seasons.length)*100;
});
}
  locationTD(newData, s)

}