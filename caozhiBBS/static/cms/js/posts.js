
$(function () {
   $('.high-light') .click(function (event) {
       var self=$(this);
       var tr=self.parent().parent();
       var post_id=tr.attr('data-id');
       var highlight=parseInt(tr.attr('data-highlight'));  //将获取出来值转换成整形
       var url='';

       if (highlight){
           url='/cms/unhighlight/'
       }else{
           url='/cms/highlight/'
       }
       zlajax.post({
           'url':url,
           'data':{
               'post_id':post_id,
           },
           'success':function (data) {
               if (data['code']==200){
                   zlalert.alertSuccessToast(message='操作成功')
                   setTimeout(function () {
                       window.location.reload();
                   },700);

               }else {
                   zlalert.alertInfo(data['message']);
               }

           },

       })

   });
});