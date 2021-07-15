$(document).ready(function(){
    users = {{users | tojson}};
    var data = "<div class='form-check'>";
    $.each(users, function(index, value){
                    data += "<input class='form-check-input' name='userlist' type='checkbox' value=" + value[0] +">" + 
                    "<label for='userlist'>" + " " + value[0] + " " + value[1] + " " + value[2] +" </label><br>";
                });
    $("#datalistusers").html(data);
    $("#user-search").on("input", function(e){
        data = "";
       $("#datalistusers").empty();
        userSearched = $("#user-search").val();
        $.ajax({
            method:"post",
            url:"/usearch",
            data:{dataPassed:userSearched},
            success:function(uSearch){
            if(uSearch.length == 0){
                    data += "<div class='no-data'>" +"Nu s-a gasit nimic..." + "</div>";
                }
                console.log(uSearch);
                $.each(uSearch, function(index, value){
                    data += "<input class='form-check-input' name='userlist' type='checkbox' value=" + value[0] +">" +  
                    "<label for='userlist'>" + " " + value[0] + " " + value[1] + " " + value[2] +" </label><br>";
                });
                data += "</div>";
                $("#datalistusers").html(data);
            }
        });
    });
});


$(document).ready(function(){
    prods = {{products | tojson}};
    var data = "<div class='form-check'>";
     $.each(prods, function(index, value){
                    data += "<input class='form-check-input' name='prodlist' type='checkbox' value="+ value[0] +">" + 
                    "<label for='prodlist'>" + " " + value[0] + " " + value[1] + " </label><br>";
                });
     $("#datalistprods").html(data);
      $("#prod-search").on("input", function(e){
        data = "";
       $("#datalistprods").empty();
        prodSearched = $("#prod-search").val();
        $.ajax({
            method:"post",
            url:"/psearch",
            data:{pdataPassed:prodSearched},
            success:function(pSearch){
                console.log(pSearch);
                if(pSearch.length == 0){
                    data += "<div class='no-data'>" +"Nu s-a gasit nimic..." + "</div>";
                }
                else{
                $.each(pSearch, function(index, value){
                    data += "<input class='form-check-input' name='prodlist' type='checkbox' value=" + value[0] +">" +  
                    "<label for='userlist'>" + " " + value[0] + " " + value[1]  +" </label><br>";
                });
                data += "</div>";
                }
                $("#datalistprods").html(data);
            }
        });
    });
});