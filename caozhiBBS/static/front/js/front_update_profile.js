$(function () {
   $('#user_update_profile_btn').click(function (event) {
       event.preventDefault();
       var self=$(this);

       var emailI=$('input[name="email"]');
       var QQI=$('input[name="qq_number"]');
       var realnameI=$('input[name="realname"]');
       var genderI=$('select[name="gender"]');
       var singatureI=$('#usersingature');
       var user_idI=self.attr('data-id');


       var email=emailI.val();
       var qq=QQI.val();
       var realname=realnameI.val();
       var gender=genderI.val();
       var singature=singatureI.val();

       zlajax.post({
           'url':'/uprofile/',
           'data':{
              'email':email,
               'qq':qq,
               'realname':realname,
               'gender':gender,
               'singature':singature,
               'user_id':user_idI
           },
           'success':function (data) {
              if(data['code']==200){
                  zlalert.alertSuccessToast(msg='个人信息完善成功')
                    setTimeout(function () {
                     window.location='/profile/';　
                     },300);
              }else{
                 zlalert.alertError(message=data['message'])
              }
           }
       })

   }) ;
});


$(function () {
   $('#change-avatar').click(function (event) {
       event.preventDefault();
       var dialog=$('#avatar-dialog');

       dialog.modal('show');

   })
});


$(function () {
   zlqiniu.setUp({
       'domain':'http://pa97eo8ux.bkt.clouddn.com/',
       'browse_btn':'change-avatar-btn',
       'uptoken_url':'/c/uptoken/',
       'success':function (up,file,info) {
           var imageInput=$("input[name='avatar_image_url']");
           imageInput.val(file.name);
       }


   }) ;
});


$(function () {
   $('#save-avatar-btn').click(function (event) {
       event.preventDefault();
       var avatarIput=$('input[name="avatar_image_url"]');
       var self=$(this);
       var user_id=self.attr('data-id');
       var avatar_image_url=avatarIput.val();

       zlajax.post({
           'url':/profile/,
           'data':{
               'avatar_image_url':avatar_image_url,
               'user_id':user_id
           },
           'success':function (data) {
               if (data['code']==200){
                   zlalert.alertSuccessToast(message='头像修改成功')
                   setTimeout(function () {
                       window.location.reload()
                   },800);
               }else{
                   zlalert.alertInfo(data['message'])
               }
           }
       })
   })
});