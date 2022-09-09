//发送邮箱
function doSendMail(obj) {
    var email = $.trim($("#regname").val());
    // 对邮箱地址进行校验xxx@xxx.xx
    if (!email.match(/.+@.+\..+/)) {
        alert("邮箱地址格式不正确");
        $("#regname").focus();
        return false;
    }
    $.post('/user/email_captcha', 'email=' + email, function (data) {
        if (data == 'email-invalid') {
            alert("邮箱地址格式不正确");
            $("#regname").focus();
            return false;
        } else if (data == 'send-pass') {
            alert("成功了，快去看快去看！！");
            $("#regname").attr('disabled', true); //验证码发送成功后禁止修改注册邮箱
            $(obj).attr('disabled', true);  //发送邮件按钮变成不可用
            return false;
        } else {
            alert("验证码未发送成功");
            return false;
        }
    })
}

//注册
function doReg(e) {
    //回车事件
    if(e != null && e.keyCode !=13){
        return false;
    }

    var regname = $.trim($("#regname").val());
    var regpass = $.trim($("#regpass").val());
    var regcode = $.trim($("#regcode").val());

    if (!regname.match(/.+@.+\..+/) || regpass.Length < 5) {
        alert("注册邮箱不正确或密码少于5位");
        return false;
    } else {
        //构建POST请求的正文数据
        var param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&ecode=" + regcode;
        //利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/user/register', param, function (data) {
            if (data == "ecode-error") {
                alert("验证码错误");
                $("#regcode").val(""); //清除验证码框内的值
                $("#regcode").focus(); //让验证码框获取到焦点供用户输入
            } else if (data == "up-invalid") {
                alert("用户名和密码不能少于5位");
            } else if (data == "user-repeated") {
                alert("该用户名已经被注册");
                $("#regname").focus();
            } else if (data == "register-pass") {
                alert("你成功了！！");
                setTimeout('location.reload();', 1000);
            } else if (data == 'reg-fail') {
                alert("注册失败，请联系张万森");
            }
        });
    }
}

// 登录
function doLogin(e){
    if(e !=null && e.keyCode != 13){
        return false;
    }
    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());
    if(loginname.Length < 5 || loginpass.Length<5){
        alert("用户名或密码少于5位");
        return false;
    } else{
        //构建POST请求的正文数据
        var param = "username="+loginname;
        param += "&password=" +loginpass;
        param += "&vcode=" + logincode;
        //利用jQuery框架发送POST请求，并获取到后台登录接口的响应内容
        $.post('/user/login', param,function (data){
            if (data == "vcode-error"){
                alert("验证码错误");
                $("#logincode").val(''); //清除验证码框的值
                $("#logincode").focus() ; //让验证码框获取到焦点供用户输入
            }else if(data == "login-pass"){
                    // alert("you did it");
                // //登录成功后，延迟1秒钟重新刷新当前页面
                setTimeout('location.reload();',1000);
            }else if(data == "login-fail"){
                alert("登录失败，请打电话给张万森");
            }
        });
    }
}


//显示模态框中登录面板
function showLogin() {
    $('#login').addClass("active");
    $("#reg").removeClass("active");
    $('#find').removeClass("active");
    $('#loginpanel').addClass("active");
    $('#regpanel').removeClass("active");
    $('#findpannl').removeClass("active");
    $('#staticBackdrop').modal('show');
}

//显示模态框中的注册面板
function showReg() {
    $('#login').removeClass("active");
    $("#reg").addClass("active");
    $('#find').removeClass("active");
    $('#loginpanel').removeClass("active");
    $('#regpanel').addClass("active");
    $('#findpannl').removeClass("active");
    $('#staticBackdrop').modal('show');
}

// 显示模态框中的找回密码面板
function showReset() {
    $('#login').removeClass("active");
    $("#reg").removeClass("active");
    $('#find').addClass("active");
    $('#loginpanel').removeClass("active");
    $('#regpanel').removeClass("active");
    $('#findpannl').addClass("active");
    $('#staticBackdrop').modal('show');
}

//