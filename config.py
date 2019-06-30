import os

DEBUG = True
CSRF_ENABLED = True    # CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护
SECRET_KEY = 'you-will-never-guess'  # 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/holiday'   # 是 Flask-SQLAlchemy 扩展需要的。这是我们数据库文件的路径
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')   # 是文件夹，我们将会把 SQLAlchemy-migrate 数据文件存储在这里。
print(SQLALCHEMY_DATABASE_URI)



