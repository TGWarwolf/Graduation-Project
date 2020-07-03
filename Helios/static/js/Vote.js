function str_pad( hex ){

	var zero = '00';
	var tmp = 2-hex.length;
	return zero.substr(0,tmp) + hex;

}

function create_ballot(id,qst_num){
	var ballot = "";
	for (i=0; i<qst_num; i++) {
		var radios = document.getElementById("qst"+i.toString());
		var value=0;
		for(j=0;j<radios.childElementCount;j++){
			if (radios.children[j].children[0].children[0].children[0].checked) {
				ballot=ballot+str_pad(j.toString(16));
			}
		}
	}
	var bjson=ballot;
	var binfo=new XMLHttpRequest();
	binfo.open('POST', '/api/create_ballot/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	binfo.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	binfo.send(JSON.stringify(bjson));//发送请求 将json写入send中

	binfo.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (binfo.readyState == 4 && binfo.status == 200) {//验证请求是否发送成功
			var result = binfo.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
}
function create_ballot2(id,qst_num,pkey){
	var ballot = "";
	for (i=0; i<qst_num; i++) {
		var radios = document.getElementById("qst"+i.toString());
		var value=0;
		for(j=0;j<radios.childElementCount;j++){
			if (radios.children[j].children[0].children[0].children[0].checked) {
				ballot=ballot+str_pad(j.toString(16));
			}
		}
	}
/*
	var curve="sm2";
	var msgData=CryptoJS.enc.Utf8.parse(ballot)
	var cipherMode = 1;//c1c2c3	
	var cipher = new SM2Cipher(cipherMode);
	var pubkeyHex = pkey;
    if (pubkeyHex.length > 130) {
        pubkeyHex = pubkeyHex.substr(pubkeyHex.length - 130);
    }
	var userKey = cipher.CreatePoint(pubkeyHex);
	msgData = cipher.str2Bytes(msgData.toString());
	var encryptData = cipher.Encrypt(userKey, msgData);
	
*/
	const publicKey = pkey;
	const encryptData = smEncrypt.sm2.doEncrypt( ballot, publicKey, 1)
	var bjson=encryptData;
	var binfo=new XMLHttpRequest();
	binfo.open('POST', '/api/create_ballot2/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	binfo.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	binfo.send(JSON.stringify(bjson));//发送请求 将json写入send中

	binfo.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (binfo.readyState == 4 && binfo.status == 200) {//验证请求是否发送成功
			var result = binfo.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
}

function doCrypt() {
            var f1 = document.form1;

            var curve = f1.curve1.value;
            var msg = f1.msg1.value;
            var msgData = CryptoJS.enc.Utf8.parse(msg);

            var pubkeyHex = f1.pubkey1.value;
            if (pubkeyHex.length > 130) {
                pubkeyHex = pubkeyHex.substr(pubkeyHex.length - 130);
            }

            var cipherMode = f1.cipherMode.value;

            var cipher = new SM2Cipher(cipherMode);
            var userKey = cipher.CreatePoint(pubkeyHex);

            msgData = cipher.str2Bytes(msgData.toString());

            var encryptData = cipher.Encrypt(userKey, msgData);
            f1.sigval1.value = encryptData;
        }

function submit_ballot(id,ballot_exist){
	if(ballot_exist=="False"){
		alert("尚未产生投票");
		window.location.href='/vote/'+id;
	}
	
	var binfo=new XMLHttpRequest();
	binfo.open('POST', '/api/submit_ballot/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	binfo.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	binfo.send(JSON.stringify("true"));//发送请求 将json写入send中

	binfo.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (binfo.readyState == 4 && binfo.status == 200) {//验证请求是否发送成功
			var result = binfo.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
    }
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

function audit(id,index){
	bjson=new Object();
	bjson.id=id;
	bjson.bid=index;
	var binfo=new XMLHttpRequest();
	binfo.open('POST', '/api/audit/'+id, true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
	binfo.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
	binfo.send(JSON.stringify(bjson));//发送请求 将json写入send中

	binfo.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (binfo.readyState == 4 && binfo.status == 200) {//验证请求是否发送成功
			var result = binfo.responseText;//获取到服务端返回的数据
			alert(result);
		}
    }
}