// 点击图片更换验证码
$(function(){
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src,'xx',Math.random());
        self.attr('src',newsrc);
    });
});

$(function () {
    $('#sms-captcha-btn').click(function (event) {
        event.preventDefault();
        var self=$(this);
        var telephone =$("input[name='telephone']").val();
        if(!(/^1[345879]\d{9}$/.test(telephone))){
            zlalert.alertInfoToast('请输入正确的手机号码');
            return;
        }
        var timestamp=(new Date).getTime();
        var sign=md5(timestamp+telephone+'caozhi1993');
        zlajax.post({
            'url':'/c/sms_captcha/',
            'data':{
                'telephone':telephone,
                'timestamp':timestamp,
                'sign':sign

            },
             'success':function (data) {
               if (data['code']==200){
                   zlalert.alertSuccessToast('短信验证码发送成功');
                   self.attr('disabled','disabled');
                   var timeCount=60
                   var timer=setInterval(function () {      //设置倒计时，需要用到setInterval函数
                       timeCount--;
                       self.text(timeCount);
                       if(timeCount<=0){
                           self.removeAttr('disabled');
                           clearInterval(timer);//数字倒计时完成后清除
                           self.text('发送验证码');
                       }

                   },1000);  //1000是间隔时间
               }else{
                   zlalert.alertInfoToast(data['message']);
               }
             }
        });
    });

});

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_input=$("input[name='telephone']");
        var sms_captcha_input=$("input[name='sms_captcha']");
        var username_input=$("input[name='username']");
        var password_input=$("input[name='password']");
        var confirm_pwd_input=$("input[name='confirmpwd']");
        var graph_captcha_input=$("input[name='graph-captcha']");

        var telephone=telephone_input.val();
        var sms_captcha=sms_captcha_input.val();
        var username=username_input.val();
        var password=password_input.val();
        var confirmpwd=confirm_pwd_input.val();
        var graph_captcha=graph_captcha_input.val();

        zlajax.post({
           'url':'/regist/',
            'data':{
               'telephone':telephone,
                'sms_captcha':sms_captcha,
                'username':username,
                'password':password,
                'confirmpwd':confirmpwd,
                'graph_captcha':graph_captcha
            },
            'success':function (data) {
                if (data['code']==200){
                    var return_to=$('#return_to_span').text();
                    if(return_to){
                        window.location=return_to;
                    }else {
                        window.location='/';
                    }
                }else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function () {
               zlalert.alertNetworkError();

            }
        });

    })
    
});

