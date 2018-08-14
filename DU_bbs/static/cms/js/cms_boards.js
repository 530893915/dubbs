/**
 * Created by Administrator on 2018/8/2.
 */

// CMS-板块管理-btn：添加新板块
$(function () {
   $('#add-board-btn').click(function (event) {
       event.preventDefault();
       xtalert.alertOneInput({
          'text':'请输入板块名称',
           'placeholder':'板块名称',
           'confirmCallback':function (inputValue) {
               xtajax.post({
                   'url':'/add_board/',
                   'data':{
                       'name':inputValue
                   },
                   'success':function (data) {
                       if(data['code']==200){
                           xtalert.alertSuccessToast('恭喜！板块添加成功！');
                           setTimeout(function () {
                               window.location.reload();
                           },500);
                       }else{
                            xtalert.alertInfoToast(data['message']);
                        }
                   }
               });
           }
       });
   });
});

// CMS-板块管理-btn：编辑
$(function () {
   $('.edit-board-btn').click(function (event) {
       event.preventDefault();
       var board_id = $(this).attr('data-board-id');

       xtalert.alertOneInput({
          'text':'请输入板块名称',
           'placeholder':'板块名称',
           'confirmCallback':function (inputValue) {
               xtajax.post({
                   'url':'/edit_board/',
                   'data':{
                       'name':inputValue,
                       'board_id':board_id
                   },
                   'success':function (data) {
                       if(data['code']==200){
                           xtalert.alertSuccessToast('恭喜！板块修改成功！');
                           setTimeout(function () {
                               window.location.reload();
                           },500);
                       }else{
                            xtalert.alertInfoToast(data['message']);
                        }
                   }
               });
           }
       });
   });
});

// CMS-板块管理-btn：删除
$(function () {
    $('.delete-board-btn').click(function (event) {
        event.preventDefault();
        var board_id = $(this).attr('data-board-id');

        xtalert.alertConfirm({
            'msg': '您确定要删除本板块吗？',
            'confirmCallback': function () {
                xtajax.post({
                    'url': '/delete_board/',
                    'data': {
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('恭喜！板块删除成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },500);
                        }else{
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});