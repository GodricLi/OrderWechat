;
let food_cat_set_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $('.wrap_cat_set .save').click(function () {
            let btn_target = $(this);
            if (btn_target.hasClass('disabled')) {
                common_ops.alert("正在处理!请勿重复提交！");
                return;
            }

            let name = $('.wrap_cat_set input[name=name]').val();
            let weight = $('.wrap_cat_set input[name=weight]').val();

            if (name.length < 1) {
                common_ops.tip('请输入正确的分类名');
                return false
            }

            if (parseInt(weight) < 1) {
                common_ops.tip('权重值必须大于1');
                return false
            }
            btn_target.addClass('disabled');

            let data = {
                name: name,
                weight: weight,
                id: $('.wrap_cat_set input[name=id]').val()
            };

            $.ajax({
                url: common_ops.buildUrl('/food/cat-set'),
                type: "POST",
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    let callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/food/cat');
                        }
                    }
                    common_ops.alert(res.msg, callback)
                }

            })

        })
    }
};

$(document).ready(function () {
    food_cat_set_ops.init()
});