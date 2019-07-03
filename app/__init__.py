from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
# from flask_bootstrap import Bootstrap

app = Flask(__name__)
# 导入指定的配置对象
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请先登录系统！'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(user_id)


from app import views, api