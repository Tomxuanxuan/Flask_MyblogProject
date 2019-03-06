#项目启动管理文件
#encoding: utf-8


from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from flask_sqlalchemy import SQLAlchemy

import pymysql
from blog import app
pymysql.install_as_MySQLdb()



#数据库
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'Flask_Myblog'
USERNAME = 'root'
PASSWORD = 'XXXXXX'  ###
DB_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/Flask_Myblog'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#设置程序的启动模式为调试模式
app.config['DEBUG'] = True


db = SQLAlchemy(app)

manager = Manager(app)

migrate = Migrate(app, db)

#添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()

