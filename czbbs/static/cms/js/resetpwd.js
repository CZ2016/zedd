
$(function () {
    $('#submit').click(function (event) {
        // event.preventDefault()
        //阻止按钮默认提交表单的事件
        event.preventDefault();
        var oldpwdE=$("input[name=oldpwd]");
        var newpwdE=$("input[name=newpwd]");
        var confirmpwdE=$("input[name=confirmpwd]");

        var oldpwd=oldpwdE.val();
        var newpwd=newpwdE.val();
        var confirmpwd=confirmpwdE.val();

        //1.要在模板的meta标签中渲染一个csrf-token
        //2.在ajax请求头部中设置X-CSRFtoken
       zlajax.post(
            {
                'url':'/cms/resetpwd/',
                'data':{
                    'oldpwd':oldpwd,
                    'newpwd':newpwd,
                    'confirmpwd':confirmpwd
                },
                'success':function (data) {
                   if (data['code'] == 200){
                       zlalert.alertSuccessToast('恭喜,密码修改成功!')
                       oldpwdE.val('');
                       newpwdE.val('');
                       confirmpwdE.val('');
                   }else{
                       var message=data['message'];
                       zlalert.alertInfo(message);
                   }
                    
                },
                'fail':function (error) {
                    zlalert.alertNetworkError();
                    }
        });
    });
});