///////////////////////Fill The Select Tags//////////////////

var populate_select =function (url, selectTag ){
    
    $.ajax({
             beforeSend: function (request) {
                        request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
                     },
            url: url,
            accepts: 'application/json',
            dataType: 'json',
            data: "",
            type: "GET",
             success: function(data){
                var opts = $.parseJSON(data);
                    $.each(opts, function(i, d) {
                       $(selectTag).append('<option value="' + d[0] + '">' + d[0] + '</option>');
                       if(selectTag == "#emptyDropdown"){
                            $("#emptyDropdown3").append('<option value="' + d[0] + '">' + d[0] + '</option>');
                            $("#emptyDropdown5").append('<option value="' + d[0] + '">' + d[0] + '</option>');
                        }
                    });
            
            }
    });
};




populate_select("/agenciesid", "#emptyDropdown" );

$('#emptyDropdown').on('change',function(){
   var optionsVal = this.options[this.selectedIndex].value;
   
});

$('#emptyDropdown3').on('change',function(){
   var optionsVal = this.options[this.selectedIndex].value;
   
   if (optionsVal != "all"){
       populate_select("/agenciesyear/"+ optionsVal , "#emptyDropdown4" );
   
   
   }
});

$('#emptyDropdown5').on('change',function(){
   var optionsVal = this.options[this.selectedIndex].value;
   
   if (optionsVal != "all"){
       populate_select("/agenciesyear/"+ optionsVal , "#emptyDropdown6" );
   
   
   }
});




//////////////////////////////SET COOKIES ///////////////////////////

function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = "name=; expires=Thu, 18 Dec 2013 12:00:00 GMT; path=/";
}




/////////////////////////LOGOUT ////////////////////////////

const button = document.getElementById('post-btn');

button.addEventListener('click', async _ => {


  try {     
    const response = await fetch('/logout/access', {
      method: 'post',
      headers: {
        authorization: "Bearer " +localStorage.getItem('token'),
      }
    }).then((response) => {
        if (response.statusText === "OK"){

            localStorage.setItem('token', '');
            setCookie(("name","",0));
            window.location.href = "/signin";
            }
         else {
            localStorage.setItem('token', '');
            setCookie(("name","",0));
            window.location.href = "/signin";
        }
        });
 
    
  } catch(err) {
    
    }
});


////////////////////////////////////// FUNCTIONS TO FILL THE TABLE FLOW CASH REPORT ///////////////



$("#tableFillCash").click(function(){

        $("#tableFillCashSelect").toggle();
        var aux = $('#toggleCash2').html();
        if (aux !=1){
            
            $('#toggleCash2').text("1");
            //
        }else{        
            $('#toggleCash2').text("1");
            $('#TableCashToggle').toggle();
           
        }

})


$('#getcashreport').click(function(){

        var aux = $('#toggleCash').html();
        
        if (aux ==1){
            $('#toggleCash').text("0");
          $("#appendTableCash > div").empty();
        }else{
            $('#toggleCash').text("1");
        }

        appendTableCash( function() {
          fillTableCash();
        });
   });




function appendTableCash( callback){

    var auxc = $('#toggleCash').html();
    if (auxc !=100000){
        $('#toggleCash').text("1");
        var para = document.createElement("DIV");
        para.innerHTML = '      <div class="card mb-3"><div class="card-header">          <i class="fa fa-table"></i> Last 5 years of net cash flows By Agencies</div>  <div class="card-body"> <div class="table-responsive">            <table class="table table-bordered" id="dataTableCash" width="100%" cellspacing="0">              <thead><tr> </tr> </thead><tfoot>            <tr>     </tr>           </tfoot>          <tbody id="customer-table">        <tr>         <td>Cedric Kelly</td>                  <td>Senior Javascript Developer</td>      </tr>           <tr>            <td>Airi Satou</td><td>Accountant</td>    </tr> </tbody>         </table>         </div>   </div>      <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>      </div>';
        $("#appendTableCash").append(para);
        $('#TableCashToggle').prependTo($("#main"));
        callback();
    }
    else{
    $('#appendTableCash').toggle();
    }
};



var fillTableCash = function() {
    var url = "/cashreport"
    var urlid= $('#emptyDropdown').find(":selected").val();
    if (urlid != "all" && urlid != ""){
        url = url + "/agency/" + urlid;
    }
       
   $("#dataTableCash").DataTable({
       "processing" : true,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print'
        ],
        "ajax" : {
                        
            beforeSend: function (request) {
                        request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
            },
             url: url,
             accepts: 'application/json',
             dataType: 'json',
            dataSrc : function(json){ 
                var json = JSON.parse(json);
                var rows = [];  
                
                if (json.length <30){
                    lineChart(json);  
                }
                for (var i=0;i<json.length;i++) {
                    if (i>0) {rows.push(json[i]);}
                    else{
                        auxThead = ""
                        for (const key in json[0]) {
                            auxThead = auxThead +"<th>" +json[0][key]+ "</th>";
                        }
                        $("#appendTableCash").find("thead > tr:first-child").append(auxThead);
                        
                    };
                }            
                return rows
            }
        },
        "columns" : [ {
            "data" : "AGENCY_ID"
        }, {
            "data" : "PROD_ABBR"
        }, {
            "data" : "YEAR1"
        }, {
            "data" : "YEAR2"
        }, {
            "data" : "YEAR3"
        }, {
            "data" : "YEAR4"
        }, {
            "data" : "YEAR5"
        }]
    });
} ;




$("#tableFill").click(function(){
        var aux = $('#toggleProf2').html();
         $("#tableFillSelect").toggle();
        if (aux !=1){            
            $('#toggleProf2').text("1");
            //
        }else{        
            $('#toggleProf2').text("1");
            $('#appendTable').toggle();           
        }
        
})


////////////////////////////////////// FUNCTIONS TO FILL THE TABLE PROFITABILITY REPORT ///////////////


$('#getprofitreport').click(function(){
        var aux = $('#toggleProf').html();
        
        if (aux ==1){
            $('#toggleProf').text("0");
          $("#appendTable > div").empty();
        }else{
            $('#toggleProf').text("1");
        }
        appendTable( function() {
          fillTable();
        });
});




function appendTable( callback){
    var aux = $('#toggleProf').html();
    if (aux !=10000){
    //$('#toggleProf').text("1");
        var para = document.createElement("DIV");
        para.className = "row";
        para.innerHTML = '  <div class="col-lg-6">    <div class="card mb-3"><div class="card-header">          <i class="fa fa-table"></i> Profitability for the last 5 Year By Agencies</div>  <div class="card-body"> <div class="table-responsive">            <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">              <thead><tr>  </tr> </thead><tfoot>            <tr>         </tr>           </tfoot>          <tbody id="customer-table">        <tr>         <td>Cedric Kelly</td>                  <td>Senior Javascript Developer</td>      </tr>           <tr>            <td>Airi Satou</td><td>Accountant</td>    </tr> </tbody>         </table>         </div>   </div>      <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>      </div></div>        <div class="col-lg-6"> <div class="card mb-3" id="barChartCol" style="display:none" ><div class="card-header"> <i class="fa fa-bar-chart"></i> Profitability Chart</div> <div class="card-body"> <div class="row">  <div class="col-sm-12 my-auto">   <canvas id="myBarChart" width="100" height="50"></canvas> </div></div></div><div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div></div></div>';
        $("#appendTable").append(para).prependTo($("#main"));
        callback();
        $('#barChartCol').toggle();
    }
    else{
    }
};



var fillTable = function() {

    var url = "/profitability";
    var urlid= $('#emptyDropdown3').find(":selected").val();
    var urlyear= $('#emptyDropdown4').find(":selected").val();
    if (urlid != "all" && urlid !=""){
        url = url + "/agency/" + urlid;
        if(urlyear != "all" && urlyear !=""){
             url = url + "/year/" + urlyear;
        }
    }

   $("#dataTable").DataTable({
        
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print'
        ],
        "ajax" : {
            "url" : url,
            accepts: 'application/json',
            dataType: 'json',
            "type": "GET",
            data: "",
            beforeSend: function (request) {
                    request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
                 },
            "url" : url,
            dataSrc : function(json){
            var json = JSON.parse(json);
            drawBar(json,this);
            var rows = [];
            for (var i=0;i<json.length;i++) {
                if (i>0) rows.push(json[i]);
            }

            return rows}
        },
        "columns" : [ {
                "data" : "name"
            }, {
                "data" : "value"
        },]
    });
} ;


Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
Chart.defaults.global.defaultFontSize = 8;

// -- Function TO DRAW BAR CHART
var drawBar = function(data1, el){

var l1= [];
var v1 = [];
var auxThead =""
for (x in data1) {
    if (x !=0){
          l1.push(data1[x]["name"]);
          v1.push(data1[x]["value"]);
    }
    else{
        for (const key in data1[0]) {
            auxThead = auxThead +"<th>" +data1[0][key]+ "</th>";
        }        
    }
}

$("#appendTable").find("thead > tr:first-child").append(auxThead);
        

var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: l1,
    datasets: [{
      label: "Profitability",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: v1,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
    },
    legend: {
      display: false
    }
  }
});

}




// FUNCTION TO DRAW LINE CHART

var lineChart = function(data1){


    var canvas = document.getElementById("lineChart");
    var ctx = canvas.getContext('2d');

    var dicc_op = {}

    var l1= [];
    var v1 = [];


    var colors = ['indigo', 'blue', 'purple', 'pink', 'red', 'orange', 'yellow', 'green', 'teal', 'cyan', 'black', 'darkgreen', 'maroon', 'rosybrown', 'gray', 'olive', 'salmon', 'darkred', 'darkkhaki', 'limegreen', 'darkslateblue', 'fuchsia', 'mediumvioletred' ];
    for (x in data1) {
        if (x !=0){
            k = Object.keys(data1[x]);
            dicc_op["label"] = data1[x][k[1]];
            dicc_op['fill'] = "false";
            dicc_op['spanGaps']= "true";
            dicc_op['lineTension']= 0.1;
            dicc_op['borderColor'] = colors[x-1];
            var data_list =[];
            for (key in k){
                if (key !=0 && key !=1){
                data_list.push(data1[x][k[key]]);
                }
            }
            dicc_op["data"] = data_list;
        }


        isEmpty = !Object.keys(dicc_op).length;
        if (!isEmpty){
            l1.push(dicc_op);
            dicc_op ={};
        }
    }

    // Global Options:
    Chart.defaults.global.defaultFontColor = 'black';
    Chart.defaults.global.defaultFontSize = 8;

    var data = {
      labels: k.splice(2,7),
      datasets: l1
    };
    var myLineChart = new Chart(ctx, {
      type: 'line',
      data: data,
      
    });
}



////////////////////////////////////// FUNCTIONS TO FILL THE TABLE AGENCIES DIM REPORT ///////////////


$('#tableFillAgen').click(function(){
        appendTableAgen( function() {
          fillTableAgen();
        });
 });




function appendTableAgen( callback){

    var auxc = $('#toggleAgen').html();
    if (auxc !=1){
        $('#toggleAgen').text("1");
        var para = document.createElement("DIV");
        para.innerHTML = '      <div class="card mb-3"><div class="card-header">          <i class="fa fa-table"></i> List of Agencies Dim</div>  <div class="card-body"> <div class="table-responsive">            <table class="table table-bordered" id="dataTableAgen" width="100%" cellspacing="0">              <thead><tr> </tr> </thead><tfoot>            <tr>     </tr>           </tfoot>          <tbody id="customer-table">        <tr>         <td>Cedric Kelly</td>                  <td>Senior Javascript Developer</td>      </tr>           <tr>            <td>Airi Satou</td><td>Accountant</td>    </tr> </tbody>         </table>         </div>   </div>      <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>      </div>';
        $("#appendTableAgen").append(para).prependTo($("#main"));
        callback();    
    }
    else{
        $('#appendTableAgen').toggle();
    }
};



var fillTableAgen = function() {
   $("#dataTableAgen").DataTable({
        "processing" : true,
         dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print'
        ],
        "ajax" : {
             beforeSend: function (request) {
                    request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
                 },
            "url" : "/allagencies",
            accepts: 'application/json',
            dataType: 'json',
            dataSrc : function(json){ 
            var json = JSON.parse(json);
            var rows = [];  
                   
            for (var i=0;i<json.length;i++) {
                if (i>0) {rows.push(json[i]);}
                else{
                    auxThead = "";
                    for (const key in json[0]) {
                        auxThead = auxThead +"<th>" +json[0][key]+ "</th>";
                    }
                    $("#appendTableAgen").find("thead > tr:first-child").append(auxThead);
                    $("#appendTableAgen").find("tfoot > tr:first-child").append(auxThead);
                    
                };
            }; 
            
            return rows[0]}
        },
        "columns" : [ {
            "data" : "AGENCY_ID"
        },  {
            "data" : "PRIMARY_AGENCY_ID"
        }, {
            "data" : "VENDOR"
        }, {
            "data" : "ACTIVE_PRODUCERS"
        }, {
            "data" : "AGENCY_APPOINTMENT_YEAR"
        }, {
            "data" : "VENDOR_IND"
        }]
    });
};



////////////////////////////////////// FUNCTIONS TO FILL THE TABLE PRODUCTS DIM  REPORT ///////////////

$('#tableFillProd').click(function(){
        appendTableProd( function() {
          fillTableProd();
        });
 });



function appendTableProd( callback){

    var auxc = $('#toggleProd').html();
    if (auxc !=1){
        $('#toggleProd').text("1");
        var para = document.createElement("DIV");
        para.innerHTML = '      <div class="card mb-3"><div class="card-header">          <i class="fa fa-table"></i> List of Products Dims</div>  <div class="card-body"> <div class="table-responsive">            <table class="table table-bordered" id="dataTableProd" width="100%" cellspacing="0">              <thead><tr> </tr> </thead><tfoot>            <tr>     </tr>           </tfoot>          <tbody id="customer-table">        <tr>         <td>Cedric Kelly</td>                  <td>Senior Javascript Developer</td>      </tr>           <tr>            <td>Airi Satou</td><td>Accountant</td>    </tr> </tbody>         </table>         </div>   </div>      <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>      </div>';
        $("#appendTableProd").append(para).prependTo($("#main"));
        callback();    
    }
    else{
        $('#appendTableProd').toggle();
    }
};



var fillTableProd = function() {
   $("#dataTableProd").DataTable({
        "processing" : true,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print'
        ],
        "ajax" : {
            beforeSend: function (request) {
                    request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
            },
            "url" : "/allproducts",
            accepts: 'application/json',
            dataType: 'json',
            dataSrc : function(json){ 
            var json = JSON.parse(json);
            var rows = [];  
                   
            for (var i=0;i<json.length;i++) {
                if (i>0) {rows.push(json[i]);}
                else{
                    auxThead = "";
                    for (const key in json[0]) {
                        auxThead = auxThead +"<th>" +json[0][key]+ "</th>";
                    }
                    $("#appendTableProd").find("thead > tr:first-child").append(auxThead);
                    $("#appendTableProd").find("tfoot > tr:first-child").append(auxThead);
                    
                };
            }; 
            
            return rows}
        },
        "columns" : [ {
            "data" : "PROD_ABBR"
        },  {
            "data" : "PROD_LINE"
        }]
    });
} ;

////////////////////////////////////// FUNCTIONS TO FILL THE TABLE ALL DATA REPORT ///////////////


$('#tableFillAll').click(function(){

    $.ajax({
             beforeSend: function (request) {
                        request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
                     },
            url: "/alldata",
            data: "",
            type: "GET",
            xhrFields: {
                responseType: 'blob'
            },
             success: function(data){
                  var link=document.createElement('a');
                  link.href=window.URL.createObjectURL(data);
                  link.download="all_data_" + new Date() + ".csv";
                  link.click();
            }
    });

 });





////////////////////////////////////// FUNCTIONS TO FILL THE TABLE REVENUES DIM REPORT ///////////////


$("#tableFillRevenues").click(function(){

        $("#tableFillSelectRevenues").toggle();
        var aux = $('#toggleRevenues').html();
        if (aux !=1){
            
            $('#toggleRevenues').text("1");
            //
        }else{        
            $('#toggleRevenues').text("1");
            $('#TableRevenuesToggle').toggle();
           
        }
})



$('#getRevenuesreport').click(function(){

        var aux = $('#toggleRevenues2').html();
        if (aux ==1){
            $('#toggleRevenues2').text("0");
          $("#appendTableRevenues > div").empty();
        }else{
            $('#toggleRevenues2').text("1");
        }

        appendTableRevenues( function() {
          fillTableRevenues();
        });
   });






function appendTableRevenues( callback){

    var auxc = $('#toggleRevenues').html();
    if (auxc !=1000){
        $('#toggleRevenues').text("1");
        var para = document.createElement("DIV");
        para.innerHTML = '      <div class="card mb-3"><div class="card-header">          <i class="fa fa-table"></i> Revenues By Agencies</div>  <div class="card-body"> <div class="table-responsive">            <table class="table table-bordered" id="dataTableRevenues" width="100%" cellspacing="0">              <thead><tr> </tr> </thead><tfoot>            <tr>     </tr>           </tfoot>          <tbody id="customer-table">        <tr>         <td>Cedric Kelly</td>                  <td>Senior Javascript Developer</td>      </tr>           <tr>            <td>Airi Satou</td><td>Accountant</td>    </tr> </tbody>         </table>         </div>   </div>      <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>      </div>';
        $("#appendTableRevenues").append(para).prependTo($("#main"));
        callback();    
    }
    else{
        $('#appendTableRevenues').toggle();
    }
};


var fillTableRevenues = function() {

    var url = "/revenues";
    var urlid= $('#emptyDropdown5').find(":selected").val();
    var urlyear= $('#emptyDropdown6').find(":selected").val();
    if (urlid != "all" && urlid !=""){
        url = url + "/agency/" + urlid;
        if(urlyear != "all" && urlyear !=""){
             url = url + "/year/" + urlyear;
        }
    }


   $("#dataTableRevenues").DataTable({
        "processing" : true,
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print'
        ],
        "ajax" : {
            beforeSend: function (request) {
                    request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
                 },
            "url" : url,
            accepts: 'application/json',
            dataType: 'json',
            dataSrc : function(json){
            var json = JSON.parse(json);
            var rows = [];
            for (var i=0;i<json.length;i++) {
                if (i>0) {rows.push(json[i]);
                } else{
                    auxThead = "";
                    for (const key in json[0]) {
                        auxThead = auxThead +"<th>" +json[0][key]+ "</th>";
                    }
                    $("#appendTableRevenues").find("thead > tr:first-child").append(auxThead);
                    $("#appendTableRevenues").find("tfoot > tr:first-child").append(auxThead);
                    
                }
            };
            return rows[0]}
        },
        "columns" : [ {
            "data" : "AGENCY_ID"
        },  {
            "data" : "PROD_ABBR"
        },{
            "data" : "STATE_ABBR"
        },{
            "data" : "STAT_PROFILE_DATE_YEAR"
        },{
            "data" : "POLY_INFORCE_QTY"
        }, {
            "data" : "PRD_ERND_PREM_AMT"
        },{
            "data" : "WRTN_PREM_AMT"
        },
             
        
        ]
    });
};

////////////////////////////////////// FUNCTIONS TO FILL THE TABLE CLUSTERS REPORT ///////////////


$('#fillCluster').click(function(){

        appendTableCluster( function() {
          fillTableCluster();
        });
   });


function appendTableCluster( callback){

    var auxc = $('#toggleCluster').html();
    if (auxc !=1){
        $('#toggleCluster').text("1");
         $('#TableCluster').toggle();
        var para = document.createElement("DIV");
        para.innerHTML = '      <div class="card mb-3"><div class="card-header">          <i class="fa fa-table"></i> Cluster Number of each Agency</div>  <div class="card-body"> <div class="table-responsive">            <table class="table table-bordered" id="dataTableCluster" width="100%" cellspacing="0">              <thead><tr> <th>AGENCY_ID</th> <th>CLUSTER</th></tr> </thead><tfoot>            <tr>   <th>AGENCY_ID</th> <th>CLUSTER</th>  </tr>           </tfoot>          <tbody id="customer-table">        <tr>         <td>Cedric Kelly</td>                  <td>Senior Javascript Developer</td>      </tr>           <tr>            <td>Airi Satou</td><td>Accountant</td>    </tr> </tbody>         </table>         </div>   </div>      <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>      </div>';
        $("#appendTableCluster").append(para);
        $('#TableCluster').prependTo($("#main"));
        callback();   
        
    }
    else{
        $('#TableCluster').toggle();
    }
};    





var fillTableCluster = function(){

    $("#dataTableCluster").DataTable({
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print'
        ],
     "ajax" : {
             beforeSend: function (request) {
                        request.setRequestHeader("Authorization", 'Bearer ' +localStorage.getItem('token'));
                     },
            url: "/clustering",
            accepts: 'application/json',
            dataType: 'json',
            data: "",
            dataSrc : function(data){
                var data = $.parseJSON(data);
                
                data_cluster1 = data[1].filter(function(item){
                                return item.labels ==4

                                }).map(function(item){
                                    var coord = {}
                                    coord['x']= item.x_axis
                                    coord['y']=item.y_axis
                                    coord['id']=item.AGENCY_ID
                                    return coord;
                                });
                data_cluster2 = data[1].filter(function(item){
                                return item.labels ==1})
                                .map(function(item){
                                    var coord = {}
                                    coord['x']= item.x_axis
                                    coord['y']=item.y_axis
                                    coord['id']=item.AGENCY_ID
                                    return coord;
                                });
                data_cluster3 = data[1].filter(function(item){
                                return item.labels ==2})
                                .map(function(item){
                                    var coord = {}
                                    coord['x']= item.x_axis
                                    coord['y']=item.y_axis
                                    coord['id']=item.AGENCY_ID
                                    return coord;
                                });
                data_cluster4 = data[1].filter(function(item){
                                return item.labels ==3})
                                .map(function(item){
                                    var coord = {}
                                    coord['x']= item.x_axis
                                    coord['y']=item.y_axis
                                    coord['id']=item.AGENCY_ID
                                    return coord;
                                });
                scatter_chart(data_cluster1, data_cluster2, data_cluster3, data_cluster4);
                return data[1];

            }

        }
        ,
        "columns" : [ {
                "data" : "AGENCY_ID"
            },  {
                "data" : "labels"
            }            
            
        ]
    });

};



// FUNCTION TO DRAW SCATTER


function scatter_chart(data1, data2, data3, data4){

    var ctx = document.getElementById("myScatterChart").getContext('2d');
    var color=["#ff6384","#5959e6","#2babab","#8c4d15","#8bc34a","#607d8b","#009688"];

    var scatterChart = new Chart(ctx, {
         type: 'scatter',
         showTooltips: true,
         data:{
             datasets: [{
                 label: 'Cluster 1',
                 backgroundColor: "transparent",
                 borderColor: color[1],
                 pointBackgroundColor: color[1],
                 pointBorderColor: color[1],
                 pointHoverBackgroundColor:color[1],
                 pointHoverBorderColor: color[1],
                 data: data1


             },

             {
                 label: 'Cluster 2',
                 backgroundColor: "transparent",
                 borderColor: color[2],
                 pointBackgroundColor: color[2],
                 pointBorderColor: color[2],
                 pointHoverBackgroundColor:color[2],
                 pointHoverBorderColor: color[2],
                 data: data2
             },
             {
                 label: 'Cluster 3',
                 backgroundColor: "transparent",
                 borderColor: color[3],
                 pointBackgroundColor: color[3],
                 pointBorderColor: color[3],
                 pointHoverBackgroundColor:color[3],
                 pointHoverBorderColor: color[3],
                 data: data3
             },
            {
                 label: 'Cluster 4',
                 backgroundColor: "transparent",
                 borderColor: color[4],
                 pointBackgroundColor: color[4],
                 pointBorderColor: color[4],
                 pointHoverBackgroundColor:color[4],
                 pointHoverBorderColor: color[4],
                 data: data4
             },

             ],

         },
           options: {

                    tooltips: {
                     callbacks: {
                        label: function(tooltipItem, data) {
                            var index = tooltipItem.index;
                            var datasetIndex = tooltipItem.datasetIndex;
                            return "AGENCY_ID: " + data.datasets[datasetIndex].data[index].id;
                         }
                      }
                   },
                   title: {
                        display: true,
                        text: 'K-Means Groups of Agencies',
                        fontSize : 14
                    }

            }

    

    });

}

