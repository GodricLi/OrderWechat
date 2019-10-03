;
let mod_pwd_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $("#save").click(function () {
            let btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            let old_password = $("#old_password").val();
            let new_password = $("#new_password").val();


            if (!old_password) {
                common_ops.alert("请输入原密码~~");
                return false;
            }

            if (!new_password || new_password.length < 6) {
                common_ops.alert("请输入不少于6位的新密码~~");
                return false;
            }
            if (new_password===old_password){
                common_ops.alert("新密码不能与原密码相同~~");
                return false
            }

            btn_target.addClass("disabled");

            let data = {
                old_password: old_password,
                new_password: new_password
            };

            $.ajax({
                url: common_ops.buildUrl("/user/reset-pwd"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    let callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });


        });
    }
};

$(document).ready(function () {
    mod_pwd_ops.init();
});