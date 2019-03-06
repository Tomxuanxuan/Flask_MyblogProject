$(document).ready(function(){
    $("#up-img-touch").click(function(){
        $("#doc-modal-1").modal({width:'600px'});
    });
});
$(function() {
    'use strict';
    // 初始化
    var $image = $('#image');
    $image.cropper({
        aspectRatio: '1', //裁剪容器比例
        autoCropArea:0.8,
        preview: '.up-pre-after',
        
    });

    // 事件代理绑定事件
    $('.docs-buttons').on('click', '[data-method]', function() {
   
        var $this = $(this);
        var data = $this.data();
        var result = $image.cropper(data.method, data.option, data.secondOption);
        switch (data.method) {
            case 'getCroppedCanvas':
            if (result) {
                // 显示 Modal
                $('#cropped-modal').modal().find('.am-modal-bd').html(result);
                $('#download').attr('href', result.toDataURL('image/jpeg'));
            }
            break;
        }
    });
    
    

    // 上传图片
    var $inputImage = $('#inputImage');
    var URL = window.URL || window.webkitURL;
    var blobURL;

    if (URL) {
        $inputImage.change(function () {
            var files = this.files;
            var file;
            if (files && files.length) {

                file = files[0];
                console.log(1,file.type);

               if (/^image\/\w+$/.test(file.type)) {
                   blobURL = URL.createObjectURL(file);
                    $image.one('built.cropper', function () {
                        // Revoke when load complete
                       URL.revokeObjectURL(blobURL);
                    }).cropper('reset').cropper('replace', blobURL);
                    $inputImage.val('');
                } else {
                    window.alert('请选择图片格式的文件');
                }
            }

            // Amazi UI 上传文件显示代码
            var fileNames = '';
            $.each(this.files, function() {
                fileNames += '<span class="am-badge">' + this.name + '</span> ';
            });
            $('#file-list').html(fileNames);
        });
    } else {
        $inputImage.prop('disabled', true).parent().addClass('disabled');
    }
    
    // 绑定上传事件
    $('#up-btn-ok').on('click',function(){
        console.log(1);
    	var $modal = $('#my-modal-loading');
    	var $modal_alert = $('#my-alert');
    	var img_src=$image.attr("src");
    	if(img_src==""){
    		set_alert_info("没有选择上传的图片");
    		$modal_alert.modal();
    		return false;
    	}

    	$modal.modal();

    	var url=$(this).attr("url");
    	console.log("url:"+url,2);
    	var canvas=$("#image").cropper('getCroppedCanvas');
    	var data=canvas.toDataURL(); //转成base64
        console.log(data.toString(),3);

        $.ajax( {
                url:'/myinfos/',
                async:false,
                dataType:'json',
                type: "POST",
                data: {"fname":"photo","photo":data.toString(),},
                success: function(data){
                    console.log(data.fname);
                    $modal.modal('close');
                    $("#doc-modal-1").modal('close');
                    // set_alert_info(data.fname);
                    $modal_alert.modal();
                	// }
                },
                error: function(){
                	$modal.modal('close');
                	set_alert_info("上传文件失败了！");
                	$modal_alert.modal();
                }
         });

    });
    
});

function rotateimgright() {
$("#image").cropper('rotate', 90);
}


function rotateimgleft() {
$("#image").cropper('rotate', -90);
}

function set_alert_info(content){
	$("#alert_content").html(content);
}


function createXhr() {
    //判断浏览器对xhr的支持性
    if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    } else {
        return new ActiveXObject("Microsoft.HMLHTTP");
    }
}
function isExist() {
    var ret = true;
    var xhr = createXhr();
    url = "/checkuname?uname=" + $("[name=uname]").val();
    xhr.open('get', url, false);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if (xhr.responseText == '1') {
                $("#show").text('用户名已存在');
                ret = false
            } else if (xhr.responseText == '') {
                $("#show").text('不能为空');
            } else if (xhr.responseText == '2') {
                $("#show").text('当前昵称');
            } else {
                $("#show").text('通过')
            }
        }
    };
    xhr.send(null);
    return ret
}
//页面加载后要执行的操作
$(function () {
    //1.为uname绑定blur事件
    $("[name=uname]").blur(function () {
        isExist();
    });
});
$("#modinfos").click(function () {
    $("#modmyinfos").css("visibility", "visible");
    $("#formbk").css("visibility", "visible");
});
$("#modmyinfos .cancel").click(function () {
    $("#modmyinfos").css("visibility", "hidden");
    $("#formbk").css("visibility", "hidden");
});
function upphclose() {
    $("#modphoto").css("visibility", "hidden");
    $("#formbk").css("visibility", "hidden");
}
function check() {
    var name = $("#modmyinfos [name=uname]").val();
    var msg = $("#show").val();
    if (name == null || name == '' || msg == '用户名已存在') {
        $("#alert_content").html('用户名不能为空或被占用');
        $('#my-alert').modal();
        return false;
    }
}
function phcheck() {
    var name = $("#modphoto [name=photo]").val();
    if (name == null || name == '') {
        return false;
    }
    // alert("上传成功！");
    // return true;
}
$("#choosephoto #upphotoimg").click(function () {
    $("#choosephoto #upphoto").click();
});


 
