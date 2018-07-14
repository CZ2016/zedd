$(function () {
   $('#changepwd-btn').click(function (event) {
       event.preventDefault();
       var oldpwdI=$('input[name="oldpassword"]');
       var newpwdI=$("input[name='newpwd']");
       var confirmpwdI=$("input[name='confirmpwd']");


       var oldpwd=oldpwdI.val();
       var newpwd=newpwdI.val();
       var confirmpwd=confirmpwdI.val();
       var return_ro=$('#changepwd_return_to_span').text();


       zlajax.post({
           'url':'/changepwd/',
           'data':{
               'oldpwd':oldpwd,
               'newpwd':newpwd,
               'confirmpwd':confirmpwd
           },
           'success':function (data) {
               if(data['code']==200 ){
                    zlalert.alertSuccessToast(message='密码修改成功');
                    if(return_ro){
                        setTimeout(function () {
                            window.location=return_ro
                        },800)
                    }else{
                        setTimeout(function () {
                            window.location='/'
                        },700)
                    }
               }else{
                   zlalert.alertInfoToast(data['message'])
               }
           }
       })
   })
});