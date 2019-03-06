#存放数据表




import datetime
from flask_sqlalchemy import SQLAlchemy

from manage import db
# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64))     #用户名
    name = db.Column(db.String(30))  ### 昵称
    password = db.Column(db.String(128))
    photo = db.Column(db.String(64))
    sex = db.Column(db.String(20))     #性别
    location = db.Column(db.String(64))     #住址
    about_me = db.Column(db.String(64))     #简介
    registration_time = db.Column(db.DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  #注册时间
    isAuthen = db.Column(db.Boolean, default=False) #用户登录状态,默认为 False

    collect_articles = db.relationship('Article', secondary='collect_article', lazy='dynamic')  #用户收藏的文章
    publish_articles = db.relationship('Article', backref='publish_article', lazy='dynamic')    #用户发表的文章

    publish_images = db.relationship('ImagesUpload', backref='publish_image', lazy='dynamic')   #用户发布的图片

    ### 资源，视频 反向关联
    resources = db.relationship('Resource', backref='user', lazy="dynamic")
    videos = db.relationship('Video', backref='user', lazy="dynamic")


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auther = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.String(64))
    article_img = db.Column(db.String(64))      #文章图片
    brief = db.Column(db.Text)
    content = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)    #发布时间
    label_id = db.Column(db.Integer, db.ForeignKey('label.label_id'))   #文章标签

    read_quantity = db.Column(db.Integer, default=0)  # 文章阅读量
    like_number = db.Column(db.Integer, default=0)  # 文章点赞数

    def to_dict(self):
        dic = {
            'article_id': self.article_id,
            'auther': self.auther,
            'title': self.title,
        }
        return dic

    @staticmethod
    def isReadArticle():
        return True

class Collect_Article(db.Model):
    __tablename__ = 'collect_article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collect_article_id = db.Column(db.Integer, db.ForeignKey('article.article_id'))
    collect_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    #author_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Label(db.Model):
    '''标签表'''
    __tablename__='label'
    label_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  #标签id
    label_name = db.Column(db.String(30))  # 标签名称
    article_infos = db.relationship('Article', backref='label', lazy='dynamic')



class Atten_user(db.Model):
    '''关注用户表'''
    __tablename__ = 'atten_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    atten_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)      #关注者用户id
    atten_auther = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)    #被关注者用户id

class Comment(db.Model):
    '''文章评论表'''
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_article_id = db.Column(db.Integer, db.ForeignKey('article.article_id'), nullable=False) #回复的文章 id
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  #用户 id
    comment_content = db.Column(db.Text, nullable=False) #评论内容
    comment_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))       #评论时间


class User_Reply(db.Model):
    '''用户回复表'''
    __tablename__ = 'user_reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    replay_kuang = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False) #针对哪个框的用户发起回复
    replay_user = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  #被回复的用户 id
    replay_user_self = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) #回复的用户 id
    replay_content = db.Column(db.Text, nullable=False) #针对用户的回复内容
    replay_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #评论时间


class Message(db.Model):
    '''用户留言表'''
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    messager = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  #留言者用户 id
    messager_other = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  #被留言者用户 id
    message_time  = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #留言时间
    message_content = db.Column(db.Text, nullable=False) #留言内容


### 资源
class Resource(db.Model):
    __tablename__ = 'resource'
    rid = db.Column(db.Integer, primary_key=True)
    rname = db.Column(db.String(100), nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    rsize = db.Column(db.Integer)
    up_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def to_dict(self):
        dic = {
            'rid': self.rid,
            'rname': self.rname,
            'fname': self.fname,
            'rsize': self.rsize,
            'up_date': str(self.up_date)
        }
        return dic


### 视频
class Video(db.Model):
    __tablename__ = 'video'
    vid = db.Column(db.Integer, primary_key=True)
    vtitle = db.Column(db.String(100), nullable=False)
    savename = db.Column(db.String(100))
    vcontent = db.Column(db.String(500), nullable=True)
    up_date = db.Column(db.Date)
    hits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class ImagesUpload(db.Model):
    '''图片上传表'''
    __tablename__ = 'imagesupload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uploader = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  #图片所属用户 id
    imagename = db.Column(db.String(64))
    imagebrief = db.Column(db.String(128))  #图片简介
    imagetime = db.Column(db.DateTime, nullable=False)


