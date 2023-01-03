// alert("register.js");

function bindEmailCaptchaClick(){
        // 找到获取验证码按钮（ID选择器）
    $("#captcha-btn").click(function (event) {
        // $this：代表的是当前按钮的jquery对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        // 获取输入框中的邮箱(name选择器)
        var email = $("input[name='email']").val();

        // 发送ajax请求
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method:"GET",
            success:function(result){
                var code = result['code'];
                if(code == 200){
                    // 发送邮箱按钮倒计时
                    var countdown = 60;
                    // 开始倒计时之前，就取消按钮的点击事件
                    $this.off("click");
                    // 每间隔多少秒执行一次, 时间单位毫秒, 1000毫秒=1秒
                    var timer = setInterval(function(){
                        $this.text(countdown);
                        countdown -= 1;
                        // 倒计时结束的时候执行
                        if(countdown <= 0){
                            // 清掉定时器
                            clearInterval(timer);
                            // 将按钮的文字重新修改回来
                            $this.text("获取验证码");
                            // 重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    alert("邮箱验证码发送成功！");
                }
                else {
                    alert(result['message']);
                }
            },
            fail:function(error){
                console.log(error);
            }
        })

    });
}

// 找到按钮，绑定点击事件
// 整个网页都加载完毕后再执行这个函数
$(function () {
    bindEmailCaptchaClick();
});