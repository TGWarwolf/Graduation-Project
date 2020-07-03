<<<<<<< HEAD
function login() {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
 
    if (username.value == "") {
 
        alert("请输入用户名");
 
    } else if (pass.value  == "") {
 
        alert("请输入密码");
 
    } else if(username.value == "admin" && pass.value == "123456"){
 
        window.location.href="/";
 
    } else {
		var user_login= new Object();
		user_login.name=username.value;
		user_login.psw=hex_sha256(pass.value);
		var login_info = new XMLHttpRequest();//第一步：创建需要的对象
		login_info.open('POST', '/login', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
		login_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
		login_info.send(JSON.stringify(user_login));//发送请求 将json写入send中

		login_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (login_info.readyState == 4 && login_info.status == 200) {//验证请求是否发送成功
			var result = login_info.responseText;//获取到服务端返回的数据
			if(result=="success"){
				alert("登陆成功");
				window.location.href="/";
			}
			else if(result == "noneUser"){
				alert("用户名不存在");
			}
			else if(result == "passError"){
				alert("密码错误");
			}
		}
        }
 
    }
}
=======
function login() {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
 
    if (username.value == "") {
 
        alert("请输入用户名");
 
    } else if (pass.value  == "") {
 
        alert("请输入密码");
 
    } else if(username.value == "admin" && pass.value == "123456"){
 
        window.location.href="/";
 
    } else {
		var user_login= new Object();
		user_login.name=username.value;
		user_login.psw=hex_sha256(pass.value);
		var login_info = new XMLHttpRequest();//第一步：创建需要的对象
		login_info.open('POST', '/login', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
		login_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
		login_info.send(JSON.stringify(user_login));//发送请求 将json写入send中

		login_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (login_info.readyState == 4 && login_info.status == 200) {//验证请求是否发送成功
			var result = login_info.responseText;//获取到服务端返回的数据
			if(result=="success"){
				alert("登陆成功");
				window.location.href="/";
			}
			else if(result == "noneUser"){
				alert("用户名不存在");
			}
			else if(result == "passError"){
				alert("密码错误");
			}
		}
        }
 
    }
}
>>>>>>> 9e0dc46bdeef9af7d86a5beca9d5503fb723d091
