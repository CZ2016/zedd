
// 添加板块
$(function () {
   $('#add-board-btn').click(function (event) {
      event.preventDefault();
      zlalert.alertOneInput({
          'text':'请输入板块名称',
          'placeholder':'请输入板块名称',
          'confirmCallback':function (inputValue) {
              zlajax.post({
                 'url':'/cms/aboards/',
                  'data':{
                     'board_name':inputValue
                  },
                  'success':function (data) {
                      if(data['code']==200){
                          window.location.reload();
                      }else {
                          zlalert.alertInfo(data['message']);
                      }
                  }
              });
          }
      });

   });
});

// 编辑板块
$(function () {
   $('.edite-board-btn').click(function () {
      var self=$(this);
      var tr=self.parent().parent();
      var board_id=tr.attr('data-id');

      zlalert.alertOneInput({
          'text':'请输入新板块名称',
          'placeholder':'新板块名称',
          'confirmCallback':function (inputValue) {
              zlajax.post({
                  'url':'/cms/uboard/',
                  'data':{
                      'board_name':inputValue,
                      'board_id':board_id
                  },
                  'success':function (data) {
                      if(data['code']==200){
                          window.location.reload();
                      }else {
                          zlalert.alertInfo(data['message'])
                      }

                  }

              })

          }
      })

   });
});

// 删除板块
$(function () {
   $('.delete-board-btn').click(function () {
      var self=$(this);
      var tr=self.parent().parent();
      var board_id=tr.attr('data-id');

      zlalert.alertConfirm({
          'msg':'确认要删除该板块吗？',
          'confirmCallback':function () {
              zlajax.post({
                  'url':'/cms/dboard/',
                  'data':{
                      'board_id':board_id
                  },
                  'success':function (data) {
                      if(data['code']==200){
                          window.location.reload();
                      }else {
                          zlalert.alertInfo(data['message'])
                      }

                  }

              })

          }
      })

   });
});