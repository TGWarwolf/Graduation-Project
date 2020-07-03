from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(seconds=30*60)
app.secret_key = 'any random string'
# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/testdb'

# 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_POOL_SIZE'] = 100
#app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
# 查询时显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

scheduler=APScheduler()
scheduler.init_app(app)



from Helios import views
from Helios import models
from Helios import apis

