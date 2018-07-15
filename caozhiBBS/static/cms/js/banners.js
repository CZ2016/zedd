// 添加新轮播图操作
$(function () {
   $('#save-banner-btn').click(function (event) {
       event.preventDefault();
       var self=$(this);
       var dialog=$('#banner-dialog');
       var banner_name_input=$("input[name='banner_name']");
       var imageInput=$("input[name='image_url']");
       var linkInput=$("input[name='link_url']");
       var priorityInput=$("input[name='priority']");

       var banner=banner_name_input.val();
       var image_url=imageInput.val();
       var link_url=linkInput.val();
       var priority=priorityInput.val();
       var submitType=self.attr('data-type');
       var bannerId=self.attr('data-id');

       if(!banner||!image_url||!link_url||!priority){
           zlalert.alertInfoToast(message='请输入完整数据')
           return;
       }

       var url='';
       if (submitType=='update'){
           url='/cms/ubanners/';
       }else {
           url='/cms/abanners/';
       }


       zlajax.post({
           'url' : url,
           'data':{
               'banner_name':banner,
               'image_url':image_url,
               'link_url':link_url,
               'priority':priority,
               'banner_id':bannerId

           },
           'success':function (data) {
               dialog.modal('hide');
               if(data['code']==200){
                   // 重新加载这个页面
                  window.location.reload()
               }else{
                   zlalert.alertInfo(data['message']);
               }
           }
       })

   })

});
//添加操作,点击编辑后，再打开添加轮播图时，输入栏清空
$(function () {
    $('#add-banner').click(function (event) {
        event.preventDefault();
        var dialog=$("#banner-dialog");

        var banner_name_input=dialog.find("input[name='banner_name']");
        var imageInput=dialog.find("input[name='image_url']");
        var linkInput=dialog.find("input[name='link_url']");
        var priorityInput=dialog.find("input[name='priority']");
        var saveBtn=dialog.find("#save-banner-btn");

        banner_name_input.val('');
        imageInput.val('');
        linkInput.val('');
        priorityInput.val('');
        saveBtn.attr('data-type','none');
        saveBtn.removeAttr('data-id');

        dialog.modal('show');

        // var tr=self.parent().parent();
        // var name=tr.attr('data-name');
        // var image_url=tr.attr('data-image');
        // var link_url=tr.attr('data-link');
        // var priority=tr.attr('data-priority');






    })

});


// 编辑操作
$(function () {
    $('.edite-banner-btn').click(function (event) {
        var self=$(this);
        var dialog=$("#banner-dialog");

        dialog.modal('show');

        var tr=self.parent().parent();
        var name=tr.attr('data-name');
        var image_url=tr.attr('data-image');
        var link_url=tr.attr('data-link');
        var priority=tr.attr('data-priority');



        var banner_name_input=dialog.find("input[name='banner_name']");
        var imageInput=dialog.find("input[name='image_url']");
        var linkInput=dialog.find("input[name='link_url']");
        var priorityInput=dialog.find("input[name='priority']");
        var saveBtn=dialog.find("#save-banner-btn");

        banner_name_input.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr('data-type','update');
        saveBtn.attr('data-id',tr.attr('data-id'));


    })
    
});


$(function () {
    $('.delete-banner-btn').click(function (event) {
        var self=$(this);
        var tr=self.parent().parent();
        var banner_id=tr.attr('data-id')

        zlalert.alertConfirm(
            {
                "msg":"确定要删除这个轮播图吗?",
                'confirmCallback':function () {
                    zlajax.post({
                        'url':'/cms/dbanner/',
                        'data':{
                            'banner_id':banner_id
                        },
                        'success':function (data) {
                            if(data['code']==200){
                                window.location.reload();

                            }else{
                                zlalert.alertInfo(message=data['message'])
                            }

                        }
                    })

                }
            }

        );

    });

});

// 点击关闭重新加载页面
// $(function () {
//     $('#close-banner-btn').click(function () {
//         window.location.reload()
//     });
// });


$(function () {
   zlqiniu.setUp({
       'domain':'http://pa97eo8ux.bkt.clouddn.com/',
       'browse_btn':'upload-btn',
       'uptoken_url':'/c/uptoken/',
       'success':function (up,file,info) {
           var imageInput=$("input[name='image_url']");
           imageInput.val(file.name);
       }


   }) ;
});