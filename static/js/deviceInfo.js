function binddeviceInfoClick() {
    // 找到获取工厂信息的按钮
    $("#deviceInfo-btn").click(function (event) {
        // $this：代表的是当前按钮的jquery对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        //获取输入框中的当前工厂名
        var deviceName = $("input[name='original_name']").val();

        // 发送ajax请求,获取工厂信息
        $.ajax({
            url:"/gs/deviceInfo/deviceName?deviceName="+deviceName,
            method:"GET",
            success:function(result){
                var code = result['code'];
                if(code == 200){
                    // 获取工厂信息成功
                    // 将工厂信息填入表单
                    $("input[name='factoryName']").val(result['data']['factoryName']);
                    $("input[name='name']").val(result['data']['name']);
                    $("input[name='type']").val(result['data']['type']);
                    $("input[name='id']").val(result['data']['id']);
                    $("input[name='description']").val(result['data']['description']);
                    $("input[name='is_online']").val(result['data']['is_online']);
                    $("input[name='now_status']").val(result['data']['now_status']);
                    $("input[name='maker_name']").val(result['data']['maker_name']);
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
    binddeviceInfoClick();
});