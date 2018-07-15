$(function () {
   var ue=UE.getEditor("editor",{
       'serverUrl':'/ueditor/upload/',
       "toolbars":[
           [
           'undo', //撤销
           'redo', //重做
           'bold', //加粗
           'italic', //斜体
           'source', //源代码
           'insertcode', //代码语言
           'fontfamily', //字体
           'fontsize', //字号
           'emotion', //表情
           'simpleupload', //单图上传
           ]
            // 有几个[]，就显示几行工具栏
       ]
   });
   window.ue=ue;  //window是全局变量，给windon绑定一个ue
});


$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();

        var log_tag=$('#Log-tag').attr('data-is-logging'); //获取html内容
        if(!log_tag){
            window.location='/login/'
        }else{

            var content=window.ue.getContent();
            var post_id=$('#post-comment').attr('data-id');
            zlajax.post({
                'url':'/comment/',
                'data':{
                   'content':content,
                    'post_id':post_id,
                },

                'success':function (data) {
                    if(data['code']==200){
                        // zlalert.alertInfo(msg='发布评论成功');
                        window.location.reload();
                    }else{
                        zlalert.alertError(data['message'])
                    }

                }
            });
        }

    })
});