;
let food_index_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        let that = this;
        $('.remove').click(function () {
            that.ops("remove", $(this).attr("data"))

        });

    }
};