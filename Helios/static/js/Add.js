function validateEmail(email) {
    var re = /^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$/;
    return re.test(email.toLowerCase());
}

function submitem(id){
	var email=document.getElementById("addem");
    if (email.value == "" || !validateEmail(email.value)){
		alert("请输入正确的邮箱地址");
		
	}
    else{
        var emjson=new Object();
		emjson.email=email.value;
		var email_info = new XMLHttpRequest();
        emjson.id=id;
		email_info.open('POST', '/api/add_email/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
		email_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
		email_info.send(JSON.stringify(emjson));//发送请求 将json写入send中

		email_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (email_info.readyState == 4 && email_info.status == 200) {//验证请求是否发送成功
			var result = email_info.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
        }
	}
    
}
function deleteem(email,id){
	var emjson=new Object();
	emjson.email=email;
	var email_info = new XMLHttpRequest();
    emjson.id=id;
	email_info.open('POST', '/api/del_email/'+id, true); 
	email_info.setRequestHeader("Content-type","application/json");
	email_info.send(JSON.stringify(emjson));

	email_info.onreadystatechange = function () {
		if (email_info.readyState == 4 && email_info.status == 200) {
			var result = email_info.responseText;
			window.location.href=result;
		}
    }
    return;
}
function addop(){
	var insert=document.getElementById("add_op");
    var num=insert.childElementCount+1;
	var tr=document.createElement("tr");
	var td=document.createElement("td");
	var node=document.createElement("input");
	node.type="text";
	node.id="op"+num.toString();
	node.required=true;
	td.appendChild(node);
	tr.appendChild(td);
	insert.appendChild(tr);
	//insert.innerHTML=insert.innerHTML+"<p><input type='text'  id='op'"+num.toString()+" required /></p>";
	//insert.insertAdjacentHTML('beforeend',"<p><input type='text'  id='op'"+toString(num+3)+" required /></p>");


}
function delop(){
	var insert=document.getElementById("add_op");
    var num=insert.childElementCount;
	if(num<=2)return;
	insert.removeChild(insert.childNodes[num]); 

}

function submitqst(id){
	var question=document.getElementById("addqst");
	var options=[];
	var opadd=document.getElementById("add_op");
	var num=opadd.childElementCount;
	for(i=0;i<num;i++){
		
			var n=i+1;
			var str="op"+n.toString();
			options.push(document.getElementById(str).value);
		
		
	}

    var qstjson=new Object();
	qstjson.text=question.value;
	qstjson.options=options;
	qstjson.num=num;
	qstjson.id=id;
	var qst_info = new XMLHttpRequest();
    
	qst_info.open('POST', '/api/add_question/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	qst_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	qst_info.send(JSON.stringify(qstjson));//发送请求 将json写入send中

	qst_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (qst_info.readyState == 4 && qst_info.status == 200) {//验证请求是否发送成功
			var result = qst_info.responseText;//获取到服务端返回的数据
				window.location.href=result;
		}
    }
}
function deleteqst(question,id){
	var qstjson=new Object();
	qstjson.question=question;
	qstjson.id=id;
	var qst_info = new XMLHttpRequest();
	qst_info.open('POST', '/api/del_question/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	qst_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	qst_info.send(JSON.stringify(qstjson));//发送请求 将json写入send中

	qst_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (qst_info.readyState == 4 && qst_info.status == 200) {//验证请求是否发送成功
			var result = qst_info.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
    return;
}
function submit_vote(imm,id){
	var votejson=new Object();
	votejson.id=id;
    votejson.imm=imm;
	var vote_info = new XMLHttpRequest();
	vote_info.open('POST', '/api/submit_vote/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	vote_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	vote_info.send(JSON.stringify(votejson));//发送请求 将json写入send中

	vote_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (vote_info.readyState == 4 && vote_info.status == 200) {//验证请求是否发送成功
			var result = vote_info.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
    return;
}

function end_vote(id){
	var votejson=new Object();
	votejson.id=id;
	var vote_info = new XMLHttpRequest();
    alert("结束投票");
	vote_info.open('POST', '/api/end_vote/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	vote_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	vote_info.send(JSON.stringify(votejson));//发送请求 将json写入send中

	vote_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (vote_info.readyState == 4 && vote_info.status == 200) {//验证请求是否发送成功
			var result = vote_info.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
    return;
}

function end_audit(id){
	var binfo=new XMLHttpRequest();
	binfo.open('POST', '/api/end_audit/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	binfo.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	binfo.send(JSON.stringify("true"));//发送请求 将json写入send中

	binfo.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (binfo.readyState == 4 && binfo.status == 200) {//验证请求是否发送成功
			var result = binfo.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
}