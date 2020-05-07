
function validateEmail(email) {
    var re = /^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$/;
    return re.test(email.toLowerCase());
}
function register() {
	
	var username = document.getElementById("username");
	var email= document.getElementById("email");
    var pass = document.getElementById("password");
	var rpass = document.getElementById("rpassword");
    if (username.value == "") {
 
        alert("请输入用户名");
 
    } else if (email.value == "" || !validateEmail(email.value)){
		
		alert("请输入正确的邮箱地址");
		
	} else if (pass.value  == "") {
 
        alert("请输入密码");
 
    } else if(rpass.value  == ""){
		
		alert("请再次输入密码");
		
	}
	else if(rpass.value != pass.value){
 
        alert("两次密码不一致");
 
    } else {
		var user_reg= new Object();
		user_reg.name=username.value;
		user_reg.email=email.value;
		user_reg.psw=hex_sha256(pass.value);
		var reg_info = new XMLHttpRequest();//第一步：创建需要的对象
		reg_info.open('POST', '/register', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
		reg_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
		reg_info.send(JSON.stringify(user_reg));//发送请求 将json写入send中

		reg_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (reg_info.readyState == 4 && reg_info.status == 200) {//验证请求是否发送成功
			var result = reg_info.responseText;//获取到服务端返回的数据
			if(result=="success"){
				alert("注册成功");
				window.location.href="/";
			}
			else if(result == "duplicateEmail"){
				alert("该邮箱已被注册");
			}
			else if(result == "duplicateName"){
				alert("该用户已被注册");
			}
		}
        }
        //window.location.href="/"
 
    }
}