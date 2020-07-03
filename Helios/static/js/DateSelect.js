<<<<<<< HEAD
function DateInit(){
	var select_id=["syear","smonth","sday","shour","smin","eyear","emonth","eday","ehour","emin"];
	var server_date=new Date();
	for(var i=0;i<10;i++){
		var sobj=document.getElementById(select_id[i]);
		var loop_start=0,loop_end=0;
		switch(i%5){
			case 0:
				loop_start=server_date.getFullYear();
				loop_end=loop_start+3;
				break;
			case 1:
				loop_start=1;
				loop_end=13;
				break;
			case 2:
				loop_start=1;
				loop_end=32;
				break;
			case 3:
				loop_end=23;
				break;
			case 4:
				loop_end=59;
				break;
		}
		OptionsCreate(sobj,loop_start,loop_end)
	}
}
function DateCheck(){
	var select_id=["syear","smonth","sday","shour","smin","eyear","emonth","eday","ehour","emin"];
	var server_date=new Date();
	var Syear=document.getElementById(select_id[0]);
	var Smonth=document.getElementById(select_id[1]);
	var Sday=document.getElementById(select_id[2]);
	var Eyear=document.getElementById(select_id[5]);
	var Emonth=document.getElementById(select_id[6]);
	var Eday=document.getElementById(select_id[7]);
	MonthChange(Sday,WhichMonth(Smonth.selectedIndex+1,Syear.options[Syear.selectedIndex].value));
	MonthChange(Eday,WhichMonth(Emonth.selectedIndex+1,Eyear.options[Eyear.selectedIndex].value));
}
function OptionsCreate(sobj,loop_start,loop_end){
	for(var j=loop_start;j<loop_end;j++){
		sobj.options.add(new Option(j,j));
	}
}
function MonthChange(sobj,targetdays){
	while(sobj.length>targetdays){
		sobj.remove(sobj.length-1);
	}
	if(sobj.length<targetdays){
		OptionsCreate(sobj,sobj.length+1,targetdays+1);
	}
}
function WhichMonth(month,year){
	switch(month){
		case 2:
			if((year%4==0&&year%100!=0)|year%400==0){
				target_day=29;
			}
			else{
				target_day=28;
			}
			break;
		case 4:
		case 6:
		case 9:
		case 11:
			target_day=30;
			break;
		default:
			target_day=31;
			break;
	}
	return target_day;
}

function create(){
	var votename = document.getElementById("vname").value;
	var description= document.getElementById("vdes").value;
	var ifp=document.getElementById("ifp").checked;
	
    var syear = document.getElementById("syear").value;
	var smonth = document.getElementById("smonth").value;
	var sday = document.getElementById("sday").value;
	var shour = document.getElementById("shour").value;
	var smin = document.getElementById("smin").value;
	var eyear = document.getElementById("eyear").value;
	var emonth = document.getElementById("emonth").value;
	var eday = document.getElementById("eday").value;
	var ehour = document.getElementById("ehour").value;
	var emin = document.getElementById("emin").value;

	var start = new Date(syear,smonth-1,sday,shour,smin,0,0);
	var end = new Date(eyear,emonth-1,eday,ehour,emin,0,0);
    if(start.getTime()<end.getTime()){
		var create_vote = new Object();
		create_vote.nm = votename;
		create_vote.des = description;
		create_vote.ifp = ifp;
		create_vote.start = start;
		create_vote.end = end;

		var vote_info = new XMLHttpRequest();
		vote_info.open('POST', '/create', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
		vote_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
		vote_info.send(JSON.stringify(create_vote));//发送请求 将json写入send中

		vote_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (vote_info.readyState == 4 && vote_info.status == 200) {//验证请求是否发送成功
			var result = vote_info.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
        }
	}
	else{
		alert("请输入正确的起始时间");
	}
=======
function DateInit(){
	var select_id=["syear","smonth","sday","shour","smin","eyear","emonth","eday","ehour","emin"];
	var server_date=new Date();
	for(var i=0;i<10;i++){
		var sobj=document.getElementById(select_id[i]);
		var loop_start=0,loop_end=0;
		switch(i%5){
			case 0:
				loop_start=server_date.getFullYear();
				loop_end=loop_start+3;
				break;
			case 1:
				loop_start=1;
				loop_end=13;
				break;
			case 2:
				loop_start=1;
				loop_end=32;
				break;
			case 3:
				loop_end=23;
				break;
			case 4:
				loop_end=59;
				break;
		}
		OptionsCreate(sobj,loop_start,loop_end)
	}
}
function DateCheck(){
	var select_id=["syear","smonth","sday","shour","smin","eyear","emonth","eday","ehour","emin"];
	var server_date=new Date();
	var Syear=document.getElementById(select_id[0]);
	var Smonth=document.getElementById(select_id[1]);
	var Sday=document.getElementById(select_id[2]);
	var Eyear=document.getElementById(select_id[5]);
	var Emonth=document.getElementById(select_id[6]);
	var Eday=document.getElementById(select_id[7]);
	MonthChange(Sday,WhichMonth(Smonth.selectedIndex+1,Syear.options[Syear.selectedIndex].value));
	MonthChange(Eday,WhichMonth(Emonth.selectedIndex+1,Eyear.options[Eyear.selectedIndex].value));
}
function OptionsCreate(sobj,loop_start,loop_end){
	for(var j=loop_start;j<loop_end;j++){
		sobj.options.add(new Option(j,j));
	}
}
function MonthChange(sobj,targetdays){
	while(sobj.length>targetdays){
		sobj.remove(sobj.length-1);
	}
	if(sobj.length<targetdays){
		OptionsCreate(sobj,sobj.length+1,targetdays+1);
	}
}
function WhichMonth(month,year){
	switch(month){
		case 2:
			if((year%4==0&&year%100!=0)|year%400==0){
				target_day=29;
			}
			else{
				target_day=28;
			}
			break;
		case 4:
		case 6:
		case 9:
		case 11:
			target_day=30;
			break;
		default:
			target_day=31;
			break;
	}
	return target_day;
}

function create(){
	var votename = document.getElementById("vname").value;
	var description= document.getElementById("vdes").value;
	var ifp=document.getElementById("ifp").checked;
	
    var syear = document.getElementById("syear").value;
	var smonth = document.getElementById("smonth").value;
	var sday = document.getElementById("sday").value;
	var shour = document.getElementById("shour").value;
	var smin = document.getElementById("smin").value;
	var eyear = document.getElementById("eyear").value;
	var emonth = document.getElementById("emonth").value;
	var eday = document.getElementById("eday").value;
	var ehour = document.getElementById("ehour").value;
	var emin = document.getElementById("emin").value;

	var start = new Date(syear,smonth-1,sday,shour,smin,0,0);
	var end = new Date(eyear,emonth-1,eday,ehour,emin,0,0);
    if(start.getTime()<end.getTime()){
		var create_vote = new Object();
		create_vote.nm = votename;
		create_vote.des = description;
		create_vote.ifp = ifp;
		create_vote.start = start;
		create_vote.end = end;

		var vote_info = new XMLHttpRequest();
		vote_info.open('POST', '/create', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
		vote_info.setRequestHeader("Content-type","application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
		vote_info.send(JSON.stringify(create_vote));//发送请求 将json写入send中

		vote_info.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
		if (vote_info.readyState == 4 && vote_info.status == 200) {//验证请求是否发送成功
			var result = vote_info.responseText;//获取到服务端返回的数据
			window.location.href=result;
		}
        }
	}
	else{
		alert("请输入正确的起始时间");
	}
>>>>>>> 9e0dc46bdeef9af7d86a5beca9d5503fb723d091
}