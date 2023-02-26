function binddevicesNumClick() {
    // 找到获取工厂信息的按钮
    $("#devicesNum-btn").click(function (event) {
        // $this：代表的是当前按钮的jquery对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        //获取输入框中的操作设备数量
        const deviceNum = $("input[name='devicesNum']").val();

        // 页面跳转
        window.location.href="/ps/controls/?devicesNum="+deviceNum;

    });
}

// 找到按钮，绑定点击事件
// 整个网页都加载完毕后再执行这个函数
$(function () {
    binddevicesNumClick();
});