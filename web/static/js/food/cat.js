;
let food_cat_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        let that = this;
        $('.wrap_search select[name=status]').change(function () {
            $('.wrap_search').submit();
        });
        $('.remove').click(function () {
            that.ops('remove', $(this).attr('data'));
        });
        $('.recover').click(function () {
            that.ops('recover', $(this).attr('data'));
        });


    },

    ops: function (act, id) {
        let callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl('/food/cat-ops'),
                    type: 'POST',
                    data: {
                        act: act,
                        id: id
                    },
                    dataType: 'json',
                    success: function (res) {
                        let callback = null;
                        if (res.code === 200) {
                            callback = function () {
                                window.location.href = window.location.href;
                            }
                        }
                        common_ops.alert(res.msg, callback)

                    }
                });

            },
        };
        common_ops.confirm((act === 'remove' ? '确定删除?' : "确定恢复？"), callback)
    }
};

$(document).ready(function () {
    food_cat_ops.init()
});