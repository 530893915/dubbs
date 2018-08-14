/**
 * Created by Administrator on 2018/7/29.
 */

// CMS-CMS用户管理-添加管理员-btn：立即添加

$(function () {
   $('#submit').click(function (event) {
       event.preventDefault();

       var emailInput = $('input[name=email]');
       var usernameInput = $('input[name=username]');
       var passwordInput = $('input[name=password]');
       var selectedCheckbox = $(':checkbox:checked');

       var email = emailInput.val();
       var username = usernameInput.val();
       var password = passwordInput.val();
       var roles = [];

       selectedCheckbox.each(function (index,element) {
            var role_id = $(this).val();
            roles.push(role_id);
       });

        if(!email){
            xtalert.alertInfoToast('请输入邮箱！');
            return;
        }

        xtajax.post({
            'url':'/add_cmsuser/',
            'data':{
                'email':email,
                'username':username,
                'password':password,
                'roles':roles
            },
            'success':function (data) {
                if(data['code'] == 200){
                    emailInput.val('');
                    usernameInput.val('');
                    passwordInput.val('');
                    // 取消选中CheckBox
                    selectedCheckbox.each(function () {
                       $(this).prop('checked',false);
                    });
                    xtalert.alertSuccessToast('添加成功！');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
   });
});
