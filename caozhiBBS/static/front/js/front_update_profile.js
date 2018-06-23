$(function () {
   $('#user_update_profile_btn').click(function (event) {
       event.preventDefault();
       var self=$(this)

       var emailI=$('input[name="email"]');
       var QQI=$('input[name="qq_number"]');
       var realnameI=$('input[name="realname"]');
       var genderI=$('select[name="gender"]');
       var singatureI=$('#usersingature');
       var user_idI=self.attr('data-id')


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