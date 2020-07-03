<<<<<<< HEAD
from flask import Flask,render_template,session
from flask import request
from datetime import datetime,timedelta
from Helios import app,db
from .models import *
from flask_sqlalchemy import SQLAlchemy
import hashlib
from collections import Counter
from sqlalchemy import or_,and_
import base64
import binascii
from gmssl import sm2, sm3

# 在电子邮件列表中添加投票者email地址
@app.route('/api/add_email/<id>',methods = ['POST'])
def add_email(id):
    vote=Vote.query.filter(Vote.id==id).first();
    
    if not 'user' in session or not session['user']==vote.admin_user:
        return "/error/unable"
    usr=User.query.filter(User.name==session['user']).first();
    if usr.email==request.json['email']:
        return "不能加入自己"
    else:
        email=Email_list(email_add=request.json['email'],vote_id=vote.id)
        db.session.add_all([email])
        db.session.commit()
        return "/vote/"+str(vote.id)

# 添加投票问题
@app.route('/api/add_question/<id>',methods = ['POST'])
def add_question(id):
    vote=Vote.query.filter(Vote.id==id).first();
    if not 'user' in session or not session['user']==vote.admin_user:
        return "/error/unable"
    else:
        qst=Question(question_text=request.json['text'],options=request.json['options'],options_num=request.json['num'],vote_id=vote.id)
        db.session.add_all([qst])
        db.session.commit()
        return "/vote/"+str(vote.id)

# 删除投票者email地址
@app.route('/api/del_email/<id>',methods = ['POST'])
def del_email(id):
    vote=Vote.query.filter(Vote.id==id).first();
    if not 'user' in session or not session['user']==vote.admin_user:
        return "/error/unable"
    else:
        db.session.delete(Email_list.query.filter(and_(Email_list.email_add==request.json['email'], Email_list.vote_id==id)).first())
        db.session.commit()
        return "/vote/"+str(vote.id)

# 删除问题
@app.route('/api/del_question/<id>',methods = ['POST'])
def del_question(id):
    vote=Vote.query.filter(Vote.id==id).first();
    if not 'user' in session or not session['user']==vote.admin_user:
        return "/error/unable"
    else:
        db.session.delete(Question.query.filter(and_(Question.question_text==request.json['question'], Question.vote_id==id)).first())
        db.session.commit()
        return "/vote/"+str(vote.id)

# 保存投票并提交
@app.route('/api/submit_vote/<id>',methods = ['POST'])
def submit_vote(id):
    vote=Vote.query.filter(Vote.id==id).first();
    if vote.finish:
        return "/error/finish"
    if not 'user' in session or not session['user']==vote.admin_user:
        return "/error/unable"
    else:
        vote.complete=True
        if request.json['imm'] or datetime.now()>vote.start:
            vote.start=datetime.now()
        if vote.start>=vote.end:
            vote.end=vote.start+timedelta(hours=24)
        db.session.commit()
        return "/vote/"+str(vote.id)

# 创建选票
@app.route('/api/create_ballot/<id>',methods = ['POST'])
def create_ballot(id):
    vote=Vote.query.filter(Vote.id==id).first()
    if vote.finish:
        return "/error/finish"
    if not 'user' in session or session['user']==vote.admin_user:
        return "/error/unable"

    admin=User.query.filter(User.name==vote.admin_user).first()
    plain=request.json.encode('utf-8')
    sm2_crypt = sm2.CryptSM2(public_key=admin.pkey, private_key=admin.skey)
    cipher=sm2_crypt.encrypt(plain).hex()
    
    hash=sm3.sm3_hash(bytes.fromhex(cipher))

    blt=Ballot(cipher=cipher,hash=hash,is_valid=False,email=session['email'],vote_id=vote.id)
    ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
    if ballot:
        db.session.delete(ballot)
        db.session.commit()
    db.session.add_all([blt])
    db.session.commit()
    return "/vote/"+str(vote.id)

# 创建选票v2
@app.route('/api/create_ballot2/<id>',methods = ['POST'])
def create_ballot2(id):
    vote=Vote.query.filter(Vote.id==id).first()
    if vote.finish:
        return "/error/finish"
    if not 'user' in session or session['user']==vote.admin_user:
        return "/error/unable"

    admin=User.query.filter(User.name==vote.admin_user).first()
    sm2_crypt = sm2.CryptSM2(public_key=admin.pkey, private_key=admin.skey)
    cipher=request.json
    hash=sm3.sm3_hash(bytes.fromhex(cipher))

    blt=Ballot(cipher=cipher,hash=hash,is_valid=False,email=session['email'],vote_id=vote.id)
    ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()

    if ballot:
        db.session.delete(ballot)
        db.session.commit()
    
    db.session.add_all([blt])
    db.session.commit()
    return "/vote/"+str(vote.id)

# 提交选票
@app.route('/api/submit_ballot/<id>',methods = ['POST'])
def submit_ballot(id):
    vote=Vote.query.filter(Vote.id==id).first()
    if not 'user' in session or session['user']==vote.admin_user:
        return "/error/unable"
    ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
    if not ballot:
        return "/error/unable"
    if ballot.is_valid:
        return "/error/unable"
    ballot.is_valid=True
    db.session.commit()
    return "/vote/"+str(vote.id)

# 结束投票期
@app.route('/api/end_vote/<id>',methods = ['POST'])
def end_vote(id):
    vote=Vote.query.filter(Vote.id==id).first()
    if not 'user' in session or not session['user']==vote.admin_user:
        return "/error/unable"
    vote.finish=True
    vote.audit=True
    vote.end=datetime.now()
    blt_list=[]
    if vote.ballot:
        for blt in vote.ballot:
            if blt.is_valid:
                blt_list.append(blt.cipher)
        res=get_result(vote.ballot,User.query.filter(User.name==vote.admin_user).first().skey,len(vote.questions))
        result = [[0 for i in range(256)] for j in range(len(res))]
        for i,qsti in enumerate(res):
            for key in dict(qsti):
                result[i][int(key,16)]=dict(qsti)[key]
    shuffle=Shuffle(ballot=blt_list,result=result,vote_id=vote.id)
    shu=Shuffle.query.filter(Shuffle.vote_id==id).first()
    if shu:
        db.session.delete(shu)
        db.session.commit()
    db.session.add_all([shuffle])
    db.session.commit()
    return "/vote/"+str(vote.id)

# 结束审查
@app.route('/api/end_audit/<id>',methods = ['POST'])
def end_audit(id):
    vote=Vote.query.filter(Vote.id==id).first()
    if not 'user' in session or session['user']!=vote.admin_user:
        return "/error/unable"
    vote.audit=False
    db.session.commit()
    return "/vote/"+str(vote.id)

# 审查
@app.route('/api/audit/<id>',methods = ['POST'])
def audit(id):
    bid=request.json['bid']
    vote=Vote.query.filter(Vote.id==id).first()
    admin=User.query.filter(User.name==vote.admin_user).first()
    shuffle=Shuffle.query.filter(Shuffle.vote_id==id).first()
    ballot=shuffle.ballot[bid]
    sm2_crypt = sm2.CryptSM2(public_key=admin.pkey, private_key=admin.skey)
    plain=sm2_crypt.decrypt(bytes.fromhex(ballot))
    [h,b,result,A]=sm2_crypt.audit(plain,bytes.fromhex(ballot))
    return 'v:%s\nw:%s\nA\':%s\nA :%s' % (h,b,result,A)

# 获取投票结果
def get_result(ballot,skey,qst_num):
    plain=[]
    sm2_crypt = sm2.CryptSM2(public_key=None, private_key=skey)
    for blt in ballot:
        if blt.is_valid:
            plaintext=sm2_crypt.decrypt(bytes.fromhex(blt.cipher))
            plain.append(plaintext)
    length=len(plain[0])//2
    result=[]
    print(plain[0])
    print(plain)
    for i in range(length):
        print([j[2*i:2*i+2] for j in plain])
        result.append(Counter([j[2*i:2*i+2] for j in plain]))
    return result

=======
from flask import Flask,render_template,session
from flask import request
from datetime import datetime,timedelta
from Helios import app,db
from .models import *
from flask_sqlalchemy import SQLAlchemy
import hashlib
from collections import Counter
from sqlalchemy import or_,and_
import base64
import binascii
from gmssl import sm2, sm3

@app.route('/api/add_email/<id>',methods = ['POST'])
def add_email(id):
    vot=Vote.query.filter(Vote.id==id).first();
    
    if not 'user' in session or not session['user']==vot.admin_user:
        return "/error/unable"
    usr=User.query.filter(User.name==session['user']).first();
    if usr.email==request.json['email']:
        return "不能加入自己"
    else:
        email=Email_list(email_add=request.json['email'],vote_id=vot.id)
        db.session.add_all([email])
        db.session.commit()
        return "/vote/"+str(vot.id)

@app.route('/api/add_question/<id>',methods = ['POST'])
def add_question(id):
    vot=Vote.query.filter(Vote.id==id).first();
    if not 'user' in session or not session['user']==vot.admin_user:
        return "/error/unable"
    else:
        qst=Question(question_text=request.json['text'],options=request.json['options'],options_num=request.json['num'],vote_id=vot.id)
        db.session.add_all([qst])
        db.session.commit()
        return "/vote/"+str(vot.id)


@app.route('/api/del_email/<id>',methods = ['POST'])
def del_email(id):
    vot=Vote.query.filter(Vote.id==id).first();
    if not 'user' in session or not session['user']==vot.admin_user:
        return "/error/unable"
    else:
        db.session.delete(Email_list.query.filter(and_(Email_list.email_add==request.json['email'], Email_list.vote_id==id)).first())
        db.session.commit()
        return "/vote/"+str(vot.id)

@app.route('/api/del_question/<id>',methods = ['POST'])
def del_question(id):
    vot=Vote.query.filter(Vote.id==id).first();
    if not 'user' in session or not session['user']==vot.admin_user:
        return "/error/unable"
    else:
        db.session.delete(Question.query.filter(and_(Question.question_text==request.json['question'], Question.vote_id==id)).first())
        db.session.commit()
        return "/vote/"+str(vot.id)

@app.route('/api/submit_vote/<id>',methods = ['POST'])
def submit_vote(id):
    vot=Vote.query.filter(Vote.id==id).first();
    if vot.finish:
        return "/error/finish"
    if not 'user' in session or not session['user']==vot.admin_user:
        return "/error/unable"
    else:
        vot.complete=True
        if request.json['imm'] or datetime.now()>vot.start:
            vot.start=datetime.now()
        if vot.start>=vot.end:
            vot.end=vot.start+timedelta(hours=24)
        db.session.commit()
        return "/vote/"+str(vot.id)

@app.route('/api/create_ballot/<id>',methods = ['POST'])
def create_ballot(id):
    vot=Vote.query.filter(Vote.id==id).first()
    if vot.finish:
        return "/error/finish"
    if not 'user' in session or session['user']==vot.admin_user:
        return "/error/unable"

    admin=User.query.filter(User.name==vot.admin_user).first()
    plain=request.json.encode('utf-8')
    sm2_crypt = sm2.CryptSM2(public_key=admin.pkey, private_key=admin.skey)
    cipher=sm2_crypt.encrypt(plain).hex()
    
    hash=sm3.sm3_hash(bytes.fromhex(cipher))

    blt=Ballot(cipher=cipher,hash=hash,is_valid=False,email=session['email'],vote_id=vot.id)
    ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
    if ballot:
        db.session.delete(ballot)
        db.session.commit()
    db.session.add_all([blt])
    db.session.commit()
    return "/vote/"+str(vot.id)

@app.route('/api/create_ballot2/<id>',methods = ['POST'])
def create_ballot2(id):
    vot=Vote.query.filter(Vote.id==id).first()
    if vot.finish:
        return "/error/finish"
    if not 'user' in session or session['user']==vot.admin_user:
        return "/error/unable"

    admin=User.query.filter(User.name==vot.admin_user).first()
    sm2_crypt = sm2.CryptSM2(public_key=admin.pkey, private_key=admin.skey)
    cipher=request.json
    hash=sm3.sm3_hash(bytes.fromhex(cipher))

    blt=Ballot(cipher=cipher,hash=hash,is_valid=False,email=session['email'],vote_id=vot.id)
    ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()

    if ballot:
        db.session.delete(ballot)
        db.session.commit()
    
    db.session.add_all([blt])
    db.session.commit()
    return "/vote/"+str(vot.id)
@app.route('/api/submit_ballot/<id>',methods = ['POST'])
def submit_ballot(id):
    vot=Vote.query.filter(Vote.id==id).first()
    if not 'user' in session or session['user']==vot.admin_user:
        return "/error/unable"
    ballot=Ballot.query.filter(and_(Ballot.vote_id==id, Ballot.email==session['email'])).first()
    if not ballot:
        return "/error/unable"
    if ballot.is_valid:
        return "/error/unable"
    ballot.is_valid=True
    db.session.commit()
    return "/vote/"+str(vot.id)

@app.route('/api/end_vote/<id>',methods = ['POST'])
def end_vote(id):
    vot=Vote.query.filter(Vote.id==id).first()
    if not 'user' in session or not session['user']==vot.admin_user:
        return "/error/unable"
    vot.finish=True
    vot.audit=True
    vot.end=datetime.now()
    blt_list=[]
    if vot.ballot:
        for blt in vot.ballot:
            if blt.is_valid:
                blt_list.append(blt.cipher)
        res=get_result(vot.ballot,User.query.filter(User.name==vot.admin_user).first().skey,len(vot.questions))
        result = [[0 for i in range(256)] for j in range(len(res))]
        for i,qsti in enumerate(res):
            for key in dict(qsti):
                result[i][int(key,16)]=dict(qsti)[key]
    shuffle=Shuffle(ballot=blt_list,result=result,vote_id=vot.id)
    shu=Shuffle.query.filter(Shuffle.vote_id==id).first()
    if shu:
        db.session.delete(shu)
        db.session.commit()
    db.session.add_all([shuffle])
    db.session.commit()
    return "/vote/"+str(vot.id)

@app.route('/api/end_audit/<id>',methods = ['POST'])
def end_audit(id):
    vot=Vote.query.filter(Vote.id==id).first()
    if not 'user' in session or session['user']!=vot.admin_user:
        return "/error/unable"
    vot.audit=False
    db.session.commit()
    return "/vote/"+str(vot.id)

@app.route('/api/audit/<id>',methods = ['POST'])
def audit(id):
    bid=request.json['bid']
    vot=Vote.query.filter(Vote.id==id).first()
    admin=User.query.filter(User.name==vot.admin_user).first()
    shuffle=Shuffle.query.filter(Shuffle.vote_id==id).first()
    ballot=shuffle.ballot[bid]
    sm2_crypt = sm2.CryptSM2(public_key=admin.pkey, private_key=admin.skey)
    plain=sm2_crypt.decrypt(bytes.fromhex(ballot))
    [h,b,result,A]=sm2_crypt.audit(plain,bytes.fromhex(ballot))
    return 'v:%s\nw:%s\nA\':%s\nA :%s' % (h,b,result,A)
    
def get_result(ballot,skey,qst_num):
    plain=[]
    sm2_crypt = sm2.CryptSM2(public_key=None, private_key=skey)
    for blt in ballot:
        if blt.is_valid:
            plaintext=sm2_crypt.decrypt(bytes.fromhex(blt.cipher))
            plain.append(plaintext)
    length=len(plain[0])//2
    result=[]
    print(plain[0])
    print(plain)
    for i in range(length):
        print([j[2*i:2*i+2] for j in plain])
        result.append(Counter([j[2*i:2*i+2] for j in plain]))
    return result
    
    
>>>>>>> 9e0dc46bdeef9af7d86a5beca9d5503fb723d091
