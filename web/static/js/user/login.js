;
let user_login_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".login_wrap .do-login").click(function () {
            let btm_target = $(this);
            if (btm_target.hasClass('disabled')) {
                common_ops.alert('正在处理，请勿重复提交');
                return;
            }
            let login_name = $('.login_wrap input[name=login_name]').val();
            let login_pwd = $('.login_wrap input[name=login_pwd]').val();

            if (login_name === undefined || login_name.length < 1) {
                common_ops.alert('请输入正确的用户名');
                return;
            }
            if (login_pwd === undefined || login_name.length < 1) {
                common_ops.alert('请输入正确的密码');
                return;
            }
            btm_target.addClass('disabled');
            $.ajax({
                url: common_ops.buildUrl('/user/login'),
                type: "POST",
                data: {'login_name': login_name, 'login_pwd': login_pwd},
                dataType: 'json',
                success: function (res) {
                    btm_target.removeClass('disabled');
                    let callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            // 跳转到主页
                            window.location.href = common_ops.buildUrl('/')
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })

        })
    }
};

$(document).ready(function () {
    user_login_ops.init();
});