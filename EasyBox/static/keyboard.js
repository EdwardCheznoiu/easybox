function keyboard(){
    var key = document.getElementsByClassName("key-btn");
    var input = document.getElementById("exampleInputEmail1")
    var text = "";
    for(var i = 0; i < key.length; i++){
        (function(index){
        key[i].onclick = function(){
           
              if(index == 10){
                  text = text.slice(0, -1);
                  input.value = text;
              }
              else{
                  input.value = text + key[index].value.toUpperCase();
                  text = input.value; 
              }          
              
        }    
    })(i);
    }
    console.log(ind);
}