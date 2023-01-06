function bindfactoryInfoClick() {
    // 找到获取工厂信息的按钮
    $("#factoryInfo-btn").click(function (event) {
        // $this：代表的是当前按钮的jquery对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        //获取输入框中的当前工厂名
        var factoryName = $("input[name='original_name']").val();

        // 发送ajax请求,获取工厂信息
        $.ajax({
            url:"/gs/factoryInfo/factoryName?factoryName="+factoryName,
            method:"GET",
            success:function(result){
                var code = result['code'];
                if(code == 200){
                    // 获取工厂信息成功
                    // 将工厂信息填入表单
                    $("input[name='name']").val(result['data']['name']);
                    $("input[name='id']").val(result['data']['id']);
                    $("input[name='address']").val(result['data']['address']);
                    $("input[name='description']").val(result['data']['description']);
                    // alert(result['message']);
                }
                else {
                    alert(result['message']);
                }
            }
        })
    });
}

// 找到按钮，绑定点击事件
// 整个网页都加载完毕后再执行这个函数
$(function () {
    bindfactoryInfoClick();
});