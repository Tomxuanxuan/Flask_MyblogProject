// 搜索建议
$(function(){
  $("#keyword").keyup(function(){
    var xhr = createXhr();
    var url = "/01-search?keyword="+this.value;
    xhr.open('get',url,true);
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4&&xhr.status==200){
        var arr=JSON.parse(xhr.responseText);
        if(arr.length > 0){
          //清空 #show 里的内容
          $("#show").html('');
          $("#show").css('display','block');
          $.each(arr,function(i,obj){
            var $p=$("<p>"+obj+"</p>");//搜索建议内容
            $("#show").append($p);
          });
        }else{
          $("#show").css('display','none');
        }
      }
    }
    xhr.send(null);
  });
});
