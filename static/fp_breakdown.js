  function years_total(current_yl,years,sym,label){
    var total = 0;
    for (var i=0; i<years.length; i++) {
      if (current_yl[years[i]] != undefined) {
        if (current_yl[years[i]][sym] != undefined) {
          total += current_yl[years[i]][sym][label];
        }
      }
    }
    return total;
  }

  function slider(){

    var num = document.getElementById("myRange").value

    var svg = d3.select("#fp_svg");
    var field_data = 1002 - (8*num);
    svg.selectAll("line").remove();
    svg.append("line").attr("x1",field_data).attr("x2",field_data).attr("y1",26).attr("y2",463).style("stroke-width", 4).style("stroke", "blue")


    document.getElementById('yard_line').innerHTML=num; 
    var yl_stats = field_positions[num];    

    var years = [];
    d3.selectAll(".myCheckbox").each(function(d){
    cb = d3.select(this);
    if(cb.property("checked")){
      years.push(cb.property("value"));
      }
    });
  // yards
    var yards = [
      {id: "dl_yards", sym: 'dl'},
      {id: "dm_yards", sym: 'dm'},
      {id: "dr_yards", sym: 'dr'},
      {id: "sl_yards", sym: 'sl'},
      {id: "sm_yards", sym: 'sm'},
      {id: "sr_yards", sym: 'sr'}
      ];
    for (var i=0; i<yards.length; i++) {
        document.getElementById(yards[i].id).innerHTML = years_total(yl_stats,years,yards[i].sym,'yards__sum')
    }     


    // completion percentage
    var comp_percentage = [
      {id: "dl_comp_perc", sym: 'dl'},
      {id: "dm_comp_perc", sym: 'dm'},
      {id: "dr_comp_perc", sym: 'dr'},
      {id: "sl_comp_perc", sym: 'sl'},
      {id: "sm_comp_perc", sym: 'sm'},
      {id: "sr_comp_perc", sym: 'sr'}
      ];
    for (var i=0; i<comp_percentage.length; i++) {
        try {
        document.getElementById(comp_percentage[i].id).innerHTML = ((years_total(yl_stats,years,comp_percentage[i].sym,'complete__sum') / (years_total(yl_stats,years,comp_percentage[i].sym,'complete__sum')+years_total(yl_stats,years,comp_percentage[i].sym,'incomplete__sum')))*100).toFixed(0)
      } catch {
        document.getElementById(comp_percentage[i].id).innerHTML = ''
      }
    }

    var comps = [
      {id: "dl_comps", sym: 'dl'},
      {id: "dm_comps", sym: 'dm'},
      {id: "dr_comps", sym: 'dr'},
      {id: "sl_comps", sym: 'sl'},
      {id: "sm_comps", sym: 'sm'},
      {id: "sr_comps", sym: 'sr'}
      ];
    for (var i=0; i<comps.length; i++) {
      try {
      document.getElementById(comps[i].id).innerHTML = years_total(yl_stats,years,comps[i].sym,'complete__sum').toString() + '/' + (years_total(yl_stats,years,comps[i].sym,'complete__sum')+years_total(yl_stats,years,comps[i].sym,'incomplete__sum')).toString()
      } catch {
        document.getElementById(comps[i].id).innerHTML = ''
      }      
    }        

    // touchdowns
    var td = [
      {id: "dl_td", sym: 'dl'},
      {id: "dm_td", sym: 'dm'},
      {id: "dr_td", sym: 'dr'},
      {id: "sl_td", sym: 'sl'},
      {id: "sm_td", sym: 'sm'},
      {id: "sr_td", sym: 'sr'}
      ];
    for (var i=0; i<td.length; i++) {
      try {
      document.getElementById(td[i].id).innerHTML = years_total(yl_stats,years,td[i].sym,'touchdown__sum')
      } catch {
        document.getElementById(td[i].id).innerHTML = ''
      }      
    }     

    // interceptions
    var int = [
      {id: "dl_int", sym: 'dl'},
      {id: "dm_int", sym: 'dm'},
      {id: "dr_int", sym: 'dr'},
      {id: "sl_int", sym: 'sl'},
      {id: "sm_int", sym: 'sm'},
      {id: "sr_int", sym: 'sr'}
      ];
    for (var i=0; i<int.length; i++) {
      try {
      document.getElementById(int[i].id).innerHTML = years_total(yl_stats,years,int[i].sym,'interception__sum')
      } catch {
        document.getElementById(int[i].id).innerHTML = ''
      }      
    }

    // pick sixes
    var pick_six = [
      {id: "dl_p6", sym: 'dl'},
      {id: "dm_p6", sym: 'dm'},
      {id: "dr_p6", sym: 'dr'},
      {id: "sl_p6", sym: 'sl'},
      {id: "sm_p6", sym: 'sm'},
      {id: "sr_p6", sym: 'sr'}
      ];
    for (var i=0; i<pick_six.length; i++) {
      try {
      document.getElementById(pick_six[i].id).innerHTML = years_total(yl_stats,years,pick_six[i].sym,'pick_six__sum')
      } catch {
        document.getElementById(pick_six[i].id).innerHTML = ''
      }
    }   
                                     

    // penalties
    var pen = [
      {id: "dl_pen", sym: 'dl'},
      {id: "dm_pen", sym: 'dm'},
      {id: "dr_pen", sym: 'dr'},
      {id: "sl_pen", sym: 'sl'},
      {id: "sm_pen", sym: 'sm'},
      {id: "sr_pen", sym: 'sr'}
      ];
    for (var i=0; i<pen.length; i++) {
      try {
      document.getElementById(pen[i].id).innerHTML = years_total(yl_stats,years,pen[i].sym,'penalty__sum')
      } catch {
        document.getElementById(pen[i].id).innerHTML = ''
      }      
    } 

    var dif = [
      {id: "dl_dif", sym: 'dl'},
      {id: "dm_dif", sym: 'dm'},
      {id: "dr_dif", sym: 'dr'},
      {id: "sl_dif", sym: 'sl'},
      {id: "sm_dif", sym: 'sm'},
      {id: "sr_dif", sym: 'sr'}
      ];
    for (var i=0; i<dif.length; i++) {
      try {
      document.getElementById(dif[i].id).innerHTML = years_total(yl_stats,years,dif[i].sym,'diff__avg').toFixed(2)
      } catch {
        document.getElementById(dif[i].id).innerHTML = ''
      }      
    }     

}