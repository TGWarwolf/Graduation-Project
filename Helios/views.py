from flask import Flask,render_template,session
from flask import request,redirect, url_for, escape
from flask_sqlalchemy import SQLAlchemy
from Helios import app,db
from .models import *
from .apis import *
import hashlib
from datetime import datetime,timedelta
import random
from sqlalchemy import or_,and_
import base64
import binascii
from gmssl import sm2, func

# 首页
@app.route('/')
def index():
    return render_template("index.html",user=session['user'] if 'user' in session else 'guest')

# 投票创建页面
@app.route('/create',methods = ['POST', 'GET'])
def create():
    if request.method == 'POST' and 'user' in session:
        start=datetime.strptime(request.json['start'], "%Y-%m-%dT%H:%M:%S.%fZ")+timedelta(hours=8)
        end=datetime.strptime(request.json['end'], "%Y-%m-%dT%H:%M:%S.%fZ")+timedelta(hours=8)
        pkey=User.query.filter(User.name==session['user']).first().pkey
        vote=Vote(name=request.json['nm'],descrip=request.json['des'],is_pri=request.json['ifp'],start=start,end=end,admin_user=session['user'],\
                 admin_pkey=pkey,complete=False,finish=False,audit=False)
        db.session.add_all([vote])
        db.session.commit()
        return "/vote/"+str(vote.id)
    if 'user' in session:
        return render_template("create.html",user=session['user'] if 'user' in session else 'guest')
    return error('unlogin')

# 投票列表
@app.route('/participate',methods = ['POST','GET'])
def participate():
	return render_template("participate.html",vote_list=Vote.query.all(),user=session['user'] if 'user' in session else 'guest')

# 投票发布、修改、结束
@app.route('/vote/<id>',methods = ['POST', 'GET'])
def vote(id):
    vote=Vote.query.filter(Vote.id==id).first();
    user=session['user'] if 'user' in session else 'guest'
    if vote==None:
        return error('notfound')
    if vote.finish:
        return vote_finish(id)
    email_list=[]
    question_list=[]
    if vote.questions:
        for qst in vote.questions:
            question_list.append([qst.question_text,qst.options])
    if vote.email_list:
        for em in vote.email_list:
            email_list.append(em.email_add)
    if not 'user' in session:
        return render_template("vote_guest.html",vote=vote,questions=question_list,ballot=None)
    if not session['user']==vote.admin_user:
        ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
        return render_template("vote_guest.html",vote=vote,questions=question_list,ballot=ballot,user=user)
    return render_template("vote_admin.html",vote=vote,email=email_list,questions=question_list,user=user)

# 投票结果公示
@app.route('/finish/<id>',methods = ['POST','GET'])
def vote_finish(id):
    vote=Vote.query.filter(Vote.id==id).first();
    if vote==None:
        return error('notfound')
    if not vote.finish:
        return vote(id)
    blt_list=[]
    question_list=[]
    user=session['user'] if 'user' in session else 'guest'
    if vote.questions:
        for qst in vote.questions:
            question_list.append([qst.question_text,qst.options])
    if vote.ballot:
        for blt in vote.ballot:
            if blt.is_valid:
                blt_list.append([blt.email,blt.hash])
    result=Shuffle.query.filter(Shuffle.vote_id==id).first().result
    if not 'user' in session:
        return render_template("vote_finish.html",vote=vote,questions=question_list,ballot=None,ballot_list=blt_list,user=user,result=result)
    if not session['user']==vote.admin_user:
        ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
        return render_template("vote_finish.html",vote=vote,questions=question_list,ballot=ballot,ballot_list=blt_list,user=user,result=result)
    return render_template("vote_finish.html",vote=vote,questions=question_list,ballot=None,ballot_list=blt_list,user=user,result=result)

# 审查页面
@app.route('/audit/<id>',methods = ['POST','GET'])
def vote_audit(id):
    vote=Vote.query.filter(Vote.id==id).first()
    admin=User.query.filter(User.name==vote.admin_user).first()
    user=session['user'] if 'user' in session else 'guest'
    blt_list=Shuffle.query.filter(Shuffle.vote_id==id).first().ballot
    sm2_crypt = sm2.CryptSM2(public_key=None, private_key=admin.skey)
    code=list(map(bytes.fromhex,blt_list))
    plain_list=list(map(sm2_crypt.decrypt,code))
    if not 'user' in session:
        return render_template("vote_audit.html",vote=vote,ballot=None,ballot_list=blt_list,user=user,plain_list=plain_list)
    if not session['user']==vote.admin_user:
        ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
        return render_template("vote_audit.html",vote=vote,ballot=ballot,ballot_list=blt_list,user=user,plain_list=plain_list)
    return render_template("vote_audit.html",vote=vote,ballot=None,ballot_list=blt_list,user=user,plain_list=plain_list)
@app.route('/delete')
def delete():
    '''
    while(Question.query.all()):
        db.session.delete(Question.query.filter(Question.id!='').first())
    while(Vote.query.all()):
        db.session.delete(Vote.query.filter(Vote.id!='').first())
    while(User.query.all()):
        db.session.delete(User.query.filter(User.name!='').first())
    while(Role.query.all()):
        db.session.delete(Role.query.filter(Role.name!='').first())
    db.session.commit()
    '''
    db.drop_all(bind=None)
    db.create_all()
    return index()
# 登录页面
@app.route('/login', methods = ['POST', 'GET'])
def login():
    #error = None
    if request.method == 'POST' and not 'user' in session:
        us=User.query.filter(User.name == request.json['name']).first()
        if(us==None):
            return "noneUser"
        sha1_passwd = '%s:%s' % (us.role_id, request.json['psw'])
        if(hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()!=us.pswd):
            return "passError"
        session['user']=request.json['name']
        session['email']=us.email
        session['pass']=sha1_passwd
        session.permanent = True
        return "success"
    if 'user' in session:
        return  error('login',session['user'])
    return render_template('login.html')
# 登出
@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('email',None)
        session.pop('pass',None)
    return index()

# 注册页面
@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        ro1 = Role(name='user')
        db.session.add_all([ro1])
        db.session.commit()
        sha1_passwd = '%s:%s' % (ro1.id, request.json['psw'])
        (skey,pkey)=sm2.sm2_key_pair_gen()
        us1 = User(name=request.json['name'], email=request.json['email'],pswd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),pkey=pkey,skey=skey,role_id=ro1.id)
        if(User.query.filter(User.name == request.json['name']).first()!=None):
            return "duplicateName"
        if(User.query.filter(User.email == request.json['email']).first()!=None):
            return "duplicateEmail"
        db.session.add_all([us1])
        db.session.commit()
        return "success"
    return render_template('register.html')

# 错误页面
@app.route('/error/<type>')
def error(type,name="guest"):
    return render_template('error.html',code=type,name=name)	
