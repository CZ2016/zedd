$(function () {
   $('#focus-btn').click(function (event) {
       event.preventDefault();
       var self=$(this);
       var other_user_id=self.attr('data-id');

       zlajax.post({
           'url':'/follow/',
           'data':{
               'other_user_id':other_user_id
           },
           'success':function (data) {
               if(data['code']==200){
                   zlalert.alertSuccessToast(message='关注成功');
                   setTimeout(function () {
                       window.location.reload()
                   },800)
               }else {
                   zlalert.alertError(message=data['message'])
               }
           }

       })

   })
});


$(function () {
   $('#unfocus-btn').click(function (event) {
       event.preventDefault();
       var self=$(this);
       var other_user_id=self.attr('data-id');

       zlajax.post({
           'url':'/unfollow/',
           'data':{
               'other_user_id':other_user_id
           },
           'success':function (data) {
               if(data['code']==200){
                   zlalert.alertSuccessToast(message='取消关注');
                   setTimeout(function () {
                       window.location.reload()
                   },800)
               }else {
                   zlalert.alertError(message=data['message'])
               }
           }

       })

   })
});