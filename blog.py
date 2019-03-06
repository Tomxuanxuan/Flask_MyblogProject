#视图函数
import base64
import math

from flask import session,jsonify
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash    #密码加密
from flask import request,redirect, url_for,json
import os
from flask import Flask


app = Flask(__name__)

from app.models import *

#SECTET_KEY属性
app.config['SECRET_KEY'] = 'HelloUser'

@app.route('/friends/articles', methods=['GET','POST'])
def friends_article():
    '''展示关注的好友文章信息'''
    if request.method == 'GET':
        if 'user_id' in session:
            pageSize = 4
            page = request.args.get('page', '1')
            page = int(page)
            # 查询第page页的数据
            # 跳过（page-1）* pageSize数据，再获取前pageSize条
            user_list = Atten_user.query.filter_by(atten_user_id=session['user_id']).all()   #查询自己关注了哪些好友
            article_list = []
            for usr in user_list:
                user = User.query.filter_by(user_id=usr.atten_auther).first()    #查询出第关注的用户的信息
                articles = user.publish_articles.all()      #查询该用户所有发表的文章, 结果为[<article1>,<article2>]
                for article in articles:
                    article_list.append(article)

            # return str(article_list)

            # article_lists = Article.query.order_by(Article.publish_time.desc()).limit(pageSize).offset((page - 1) * pageSize).all()  # 按照时间顺序倒序排列
            # # 通过pageSize和总记录数计算尾页页码
            # last_page = math.ceil((db.session.query(Article).count()) / pageSize)  # ceil向上取整
            #
            # # prev_page表示上一页页码
            # if page == 1:
            #     prev_page = 1
            # else:
            #     prev_page = page - 1
            #
            # # next_page表示下一页页码
            # if page == last_page:
            #     next_page = last_page
            # else:
            #     next_page = page + 1
            #
            hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
            timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
            readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
            return render_template('index.html', article_list=article_list, params=locals())
        else:   #未登录用户,跳转到首页
            return redirect('/')


@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    # loginname = session['username']
    #变量-pageSize,表示每页所显示的记录数
    pageSize = 4
    #接收前端传递过来的请求参数page，如果没有设置为1
    #保存在变量page中
    page = request.args.get('page', '1')
    page = int(page)

    art_type = request.args.get('art_type', '0')

    if art_type == '0':

    #查询第page页的数据
    #跳过（page-1）* pageSize数据，再获取前pageSize条
        article_list = Article.query.order_by(Article.publish_time.desc()).limit(pageSize).offset((page-1)*pageSize).all()  # 按照时间顺序倒序排列

    else:
        article_list = Article.query.filter_by(label_id=art_type).order_by(db.desc(Article.publish_time)).limit(pageSize).offset((page -1)*pageSize).all()

    # 通过pageSize和总记录数计算尾页页码
    last_page = math.ceil((db.session.query(Article).count())/pageSize) #ceil向上取整

    #prev_page表示上一页页码
    if page == 1:
        prev_page = 1
    else:
        prev_page = page - 1

    #next_page表示下一页页码
    if page == last_page:
        next_page = last_page
    else:
        next_page = page + 1

    article_topblog = Article.query.order_by(db.desc(Article.like_number)).limit(3).all()

    hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()   #点赞排行
    timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()    #时间排序
    readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()   #阅读量排行
    return render_template('index.html', article_list=article_list, prev_page=prev_page, next_page=next_page, last_page=last_page, params=locals())

# @app.route('/message/insert', methods=['GET','POST'])
# def mess_insert():
#     mess = Message()
#     mess.messager = 3
#     mess.messager_other = 1
#     mess.message_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     mess.message_content = '齐心协力建家乡'
#
#     db.session.add(mess)
#     db.session.commit()
#     return 'OK'

@app.route('/message', methods=['GET','POST'])
def message():
    '''作者个人中心 留言板信息'''
    if request.method == 'GET':
        auther_id = request.args.get('auther_id')
        message_lists = Message.query.filter_by(messager_other=auther_id).order_by(Message.message_time.desc()).all()

        mess_list = []
        for message_list in message_lists:
            message = {}
            message['messager'] = User.query.filter_by(user_id=message_list.messager).first().username
            message['messager_id'] = message_list.messager
            message['message_time'] = message_list.message_time.strftime('%Y-%m-%d %H:%M:%S')
            message['message_content'] = message_list.message_content
            mess_list.append(message)
        jsmessageStr = json.dumps(mess_list)    #转换为 json 格式字符 返回
        return jsmessageStr

@app.route('/attenusershow')
def attenusershow():
    '''关注用户,与粉丝用户显示'''
    atten = request.args.get('atten')
    print(atten)
    fans = request.args.get('fans')


    if atten:
        atten_user_list = []
        res_atten = Atten_user.query.filter_by(atten_user_id=atten).all()   #关注的用户的 id
        for res_att in res_atten:
            dic_atten = {}
            dic_atten['key'] = 'atten'  # 关键字是关注
            atten_user = User.query.filter_by(user_id=res_att.atten_auther).first()
            dic_atten['user_id'] = atten_user.user_id
            dic_atten['username'] = atten_user.name
            dic_atten['photo'] = atten_user.photo
            atten_user_list.append(dic_atten)  #关注的用户详细信息字典
        attenjsonStr = json.dumps(atten_user_list)    #转换为 json 格式
        return attenjsonStr

    if fans:
        fans_user_list = []
        res_fans = Atten_user.query.filter_by(atten_auther=fans).all()  #谁关注了我
        for refans in res_fans:
            dic_fans = {}
            dic_fans['key'] = 'fans'
            fans_user = User.query.filter_by(user_id=refans.atten_user_id).first()
            dic_fans['user_id'] = fans_user.user_id
            dic_fans['username'] = fans_user.name
            dic_fans['photo'] = fans_user.photo
            fans_user_list.append(dic_fans)  #粉丝用户详细信息
        fansjsonStr = json.dumps(fans_user_list)
        return fansjsonStr


@app.route('/attenuser', methods=['GET','POST'])
def attenuser():
    '''点击按钮,关注作者'''
    if request.method == "GET":     #用来查看用户是否已经登录
        if 'user_id' not in session:    #用户未登录,返回 False
            res_atten = "False"
            return res_atten
        else:
            auther_id = request.args.get('auther_id')   #查看的作者 id,(你要关注的作者 id)
            atten_user_id = session['user_id']
            res = Atten_user.query.filter_by(atten_user_id= atten_user_id, atten_auther= auther_id).all()
            if res: #已登录,在关注表中也查到了数据
                res_atten = "True"
            else:
                res_atten = "False"
            return res_atten
    else:
        if not session['username']:     #如果未登录,跳到登录页面
            return redirect('/login')
        else:

            user_id = session['user_id']
            atten_autherId = request.args.get('atten_autherId')     #从前端将关注的用户 id 传过来
            # 先检查用户是否已经关注过
            res_atten = request.args.get('res_atten')   #从前端获取的参数True,或 False
            if res_atten == 'True':
                # 查询出要删除的实体对象,执行删除操作(取消关注)
                sel_res = Atten_user.query.filter_by(atten_user_id=user_id, atten_auther=atten_autherId).first()
                db.session.delete(sel_res)
                db.session.commit()
                return '取关成功'
            else:
                add_attenUser = Atten_user(atten_user_id=user_id, atten_auther=atten_autherId)
                db.session.add(add_attenUser)      #添加到关注数据库中
                db.session.commit()
                return '关注成功'

@app.route('/autherinfos/<auther_id>', methods=['GET', 'POST'])
def autherinfos(auther_id):
    '''作者的个人中心'''
    if request.method == 'GET':
        auther = User.query.filter_by(user_id=auther_id).first()
        art_ids = auther.publish_articles.order_by(db.desc(Article.publish_time)).all()    #将作者的个人信息与发表的文章信息渲染到前端
        fans = db.session.query(Atten_user).filter(Atten_user.atten_auther==auther_id).count()
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = 'None'
        images = ImagesUpload.query.filter_by(uploader=auther_id).order_by(db.desc(ImagesUpload.imagetime)).all()
        return render_template('authorinfo.html', params=locals())
    else:
        messager_other = auther_id  #被留言者
        messager = request.form['user_id']
        message_content = request.form['messagecontent']

        mes = Message()
        mes.messager = messager
        mes.messager_other = messager_other
        mes.message_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mes.message_content = message_content

        db.session.add(mes)
        db.session.commit()
        return '留言成功'


@app.route('/about/collect/<userID>', methods=['GET', 'POST'])
def collect(userID):
    '''我的收藏'''

    flag = 'MyCollect'
    user_info = User.query.filter_by(user_id=userID).first()    #返回查询的第一个结果的user_id，没有则返回None
    articles = user_info.collect_articles.all()  #获取到该用户所有收藏的文章 id

    return render_template('about.html', articles=articles, flag=flag)

@app.route('/about/publish/<userID>')
def PublishArticle(userID):
    '''个人中心，我的发表'''
    flag = 'MyPublish'
    user = User.query.filter_by(user_id=userID).first()
    art_ids = user.publish_articles.all()

    return render_template('about.html', articles=art_ids, flag=flag)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    '''文章编辑'''
    if request.method == 'GET':
        hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
        timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
        readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
        return render_template('release.html', params=locals())
    else:
        #发表文章
        title = request.form['title']
        label = request.form['list']
        brief = request.form['brief']
        content = request.form['wen']


        #封面图
        filename = ' '   #如果用户没有上传封面图,则图片名称赋值为空

        # fname = request.form.get('fname')
        # if fname == 'photo':
        file = request.files['photo']
        try:
            ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            ext = file.filename.split('.')[-1]
            filename = ftime + '.' + ext
            basedir = os.path.dirname(__file__)
            upload_path = os.path.join(basedir, 'static/upload', filename)
            file.save(upload_path)
        except Exception as e:
            print('上传失败', e)

        article = Article()
        article.title = title
        article.content = content
        article.brief = brief
        article.label_id = label
        article.article_img = filename
        article.publish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M%:%S')
        user = User.query.filter_by(user_id=session['user_id']).first()
        article.publish_article = user

        db.session.add(article)
        db.session.commit()

    hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
    timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
    readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
    return render_template('release.html', params=locals())

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/reply', methods=['GET', 'POST'])
def reply():
    '''用户回复'''
    # {'replay_kuang': 1, 'replay_user': 'admin', 'replay_user_self': 'python', 'replay_content':'aasdf'}
    if request.method == 'GET':
        return '错误'
    else:
        if 'user_id' not in session:
            return '请登录'
        else:
            flag = request.form['flag']
            if flag == '1':
                replay_kuang = request.form['replay_kuang']
                kuangid = request.form['replay_user']   #被回复人 kuangid
                replay_user = Comment.query.filter_by(id=kuangid).first().comment_user_id
                print(replay_user)
                replay_user_self = session['user_id']   #回复人
                replay_content = request.form['replay_content']
                replay_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                replay_user_id = request.form['replay_id']
                user_reply = User_Reply.query.filter_by(id=replay_user_id).first()
                replay_kuang = user_reply.replay_kuang
                replay_user = user_reply.replay_user_self   #被回复人
                replay_user_self = session['user_id']   #回复人
                replay_content = request.form['replay_content']
                replay_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            replyInfo = User_Reply()
            replyInfo.replay_kuang = replay_kuang
            replyInfo.replay_user = replay_user
            replyInfo.replay_user_self = replay_user_self
            replyInfo.replay_content = replay_content
            replyInfo.replay_time = replay_time
            db.session.add(replyInfo)
            db.session.commit()
            print('ok')
            return 'OK'


@app.route('/comment', methods=['GET','POST'])
def comment():
    '''用户评论表'''
    if request.method == 'GET':
        #/comment?article=1
        article_id = request.args.get('article')    #获取到文章 id
        comment_lists = Comment.query.filter_by(comment_article_id=article_id).all()    #查询到文章有哪些评论
        data_list =[]    #最后要返回的 json 数据
        for comment_list in comment_lists:
            data = {}
            user = User.query.filter_by(user_id=comment_list.comment_user_id).first() #通过 userid 查询 user
            data['comment_id'] = comment_list.id    #回复框的 id
            data['user'] = user.username #用户名
            data['image'] = user.photo #用户头像
            data['comment'] = comment_list.comment_content  #文章评论
            data['comment_time'] = comment_list.comment_time.strftime('%Y-%m-%d %H:%M:%S')

            #回复

            #查询文章评论有哪些回复
            comment_reply = User_Reply.query.filter_by(replay_kuang=comment_list.id).all()
            reply_list = []
            for comment_id in comment_reply:  #每一个回复框  [<User_Reply 1>, <User_Reply 2>]
                reply_results = comment_id    #查询每个框的回复消息
                reply = {}
                reply['replay_id'] = comment_id.id
                reply['replay_user'] = User.query.filter_by(user_id=reply_results.replay_user).first().username     #被回复用户
                reply['replay_user_self'] = User.query.filter_by(user_id=reply_results.replay_user_self).first().username  #回复者 用户名
                reply['replay_content'] = reply_results.replay_content  #回复的内容
                reply['replay_time'] = reply_results.replay_time.strftime('%Y-%m-%d %H:%M:%S')    #回复的时间

                reply_list.append(reply)    #将回复的字典装入列表

            data['replay'] = reply_list

            data_list.insert(0, data)  #将每条评论的 data 装入列表

        #转换为 json
        jsonStr = json.dumps(data_list)

        return jsonStr


        #构建一个 json 格式文本返回
        # [{用户昵称:user,
        #   用户头像:image,
        #   文章评论:comment,
        #   评论时间:time,
        #   用户回复:[{
        #       回复用户:replay_user
        #       被回复用户:replay_user_self
        #       回复内容:replay_content
        #       回复时间:replay_time
        #   },{          回复用户:replay_user
        #                被回复用户:replay_user_self
        #                回复内容:replay_content
        #                回复时间:replay_time
        #      }]
        #   },{},{}]

    else:
        if 'user_id' not in session:
            return '请先登录'
        else:
            inputText = request.form['comment'] #获取到文章评论内容
            article_id = request.args.get('article')  # 获取到文章 id
            commen_res = Comment()
            commen_res.comment_article_id = article_id
            commen_res.comment_user_id = session['user_id']
            commen_res.comment_content = inputText
            commen_res.comment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.add(commen_res)
            db.session.commit()
            return 'OK'

@app.route('/article/<article_id>', methods=['GET', 'POST'])
def show_article(article_id):
    '''文章内容 展示'''
    if request.method == 'GET':
        article_info = Article.query.filter_by(article_id=article_id).first()
        article_info.read_quantity += 1
        db.session.add(article_info)
        db.session.commit()

        article_all = Article.query.all()
        num = db.session.query(Article).count()
        for i in range(num):
            if article_info == article_all[i]:
                if i == 0:
                    up_article = article_info
                    down_article = article_all[i + 1]
                elif i == num-1:
                    up_article = article_all[i - 1]
                    down_article = article_info
                else:
                    up_article = article_all[i-1]   #上一篇文章id
                    down_article = article_all[i+1]  #下一篇文章id

        if 'user_id' in session:
            user = User.query.filter_by(user_id=session['user_id']).first()
        else:
            user = 'None'

        hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
        timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
        readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
        return render_template('info.html', article_info=article_info, user=user, uparticle=up_article, downarticle=down_article, params=locals())
    else:
        article_info = Article.query.filter_by(article_id=article_id).first()
        if 'user_id' not in session:
            islike = 'False'
            Strlike = [{"like": article_info.like_number, "islike": islike}]
            jsStrlike = json.dumps(Strlike)
            return jsStrlike
        else:
            Arti_isCollect = Collect_Article.query.filter_by(collect_user_id=session['user_id'],collect_article_id=article_id).first()      #用户是否为该文章点过赞

            like = request.args.get('like', '0')    #接收前端来的参数 like,如果没有设置为0
            if like == '1':    #点赞功能
                if Arti_isCollect:
                    #有值为真,说明用户已经收藏该文章,应该取消收藏,并将数字-1
                    db.session.delete(Arti_isCollect)
                    db.session.commit()
                    article_info.like_number -= 1

                else:
                    #没有值说明用户未收藏该文章,将文章收藏,并将赞数量+1
                    collect_article_id = article_id
                    collect_user_id = session['user_id']
                    collect_info = Collect_Article(collect_article_id=collect_article_id, collect_user_id=collect_user_id)
                    db.session.add(collect_info)
                    db.session.commit()
                    article_info.like_number += 1
                db.session.add(article_info)    #提交点赞数量
                db.session.commit()
                return 'OK'     #点赞或取消点赞成功
            else:
                if Arti_isCollect:
                    islike = "True"
                else:
                    islike = "False"
                Strlike = [{"like":article_info.like_number,"islike":islike}]
                jsStrlike = json.dumps(Strlike)
                return jsStrlike




@app.route('/login',methods=['GET','POST'])
def login_views():
    '''登录页面'''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        #接收前端传递过来的数据
        loginname = request.form.get('username')
        upwd = request.form.get('password')
        #使用接收的数据去数据库中验证-查询
        user = User.query.filter_by(username=loginname).first()
        if user:
            pwd = user.password
            res = check_password_hash(pwd, upwd)    #密码校验

        #如果用户存在的话，则将数据保存进session
            if res:
                #登录成功
                session['user_id'] = user.user_id
                session['username'] = user.username
                session['photo'] = user.photo

                user.isAuthen=True
                db.session.add(user)
                db.session.commit()

                return redirect('/friends/articles')
            else:
                errMsg = "密码不正确"
                return render_template('login.html', errMsg=errMsg)
        else:
          #登录失败
          errMsg = "用户名不正确"
          return render_template('login.html', errMsg=errMsg)

@app.route('/register/check')
def check_uname():
    '''检查用户名是否存在'''
    uname = request.args['uname']
    res_username = User.query.filter_by(username=uname).first()
    if res_username:
        errMsg = '用户名已存在'
    else:
        errMsg = ''
    return errMsg


check_number = '123321' #生成一个校验码,发到用户邮箱

@app.route('/register/checkemail')
def check_email():
    '''检查邮箱,获取验证码'''
    email_address = request.args['email']
    print(email_address)
    #先检车邮箱是否注册
    user = User.query.filter_by(email=email_address).first()
    if user:
        return render_template('register.html', errMsg='emailErr')
    else:
        from config import send_mail
        recEmail = send_mail(email_address, check_number)
        res = recEmail.mail()   #发送邮件
        return str(res)


@app.route('/register', methods=['GET','POST'])
def register():
    '''注册页面'''
    if request.method == 'GET':

        return render_template('register.html')
    else:  #从注册页面的form表中获取字段值
        check_num = request.form.get('mibao')
        email = request.form.get('email')
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password1'))    #密码加密
        registration_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 对从前端得到的数据进行校验
        #1.用户名是否已经在表中有了
        user = User.query.filter_by(username=username).first()
        if user:
            errMsg = 'usernameErr'
            return render_template('register.html', errMsg=errMsg)
        else:
            if check_num == check_number:
                user = User(email=email, username=username,name=username, password=password, registration_time=registration_time)
                # 将user添加到数据库中
                db.session.add(user)
                #提交事务
                db.session.commit()
                session['user_id'] = user.user_id
                session['username'] = user.username
                session['photo'] = user.photo
                #注册成功跳转到主页
                return redirect(url_for('index'))
            else:
                return render_template('register.html', errMsg='emailCheckErr')

### video
@app.route('/video')
def video_views():
    videos = db.session.query(Video).order_by("vid desc").all()
    hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
    timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
    readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
    return render_template('video.html', videos=videos, params=locals())

@app.route('/videoinfo/<vid>')
def videoinfo(vid):
    if request.method == "GET":
        video = db.session.query(Video).filter_by(vid=vid).first()
        auther = db.session.query(User).filter_by(user_id=video.user_id).first()
        # user = User.query.filter_by(user_id=session['user_id']).first()

        return render_template("videoinfo.html", video=video, auther=auther)


@app.route('/myinfos/', methods=['GET', 'POST'])
def myinfos():
    '''用户个人中心'''
    if request.method == 'POST':
        fname = request.form.get('fname')
        if fname == 'photo':
            try:
                photo = request.form.get('photo')
                img = base64.b64decode(photo.split(',')[-1])
                ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                ext = photo.split(';')[0].split('/')[-1]
                filename = ftime + '.' + ext
                basedir = os.path.dirname(__file__)
                upload_path = os.path.join(basedir, 'static/upload', filename)
                f = open(upload_path, 'wb')
                f.write(img)
                f.close()
                user = User.query.get(session['user_id'])
                user.photo = filename
                print(user.photo)
                db.session.add(user)
                db.session.commit()
                return json.dumps({"fname":filename})
            except Exception as e:
                print('上传失败', e)
        else:
            name = request.form.get('uname')
            sex = request.form.get('sex')
            email = request.form.get('email')
            address = request.form.get('address')
            intro = request.form.get('intro')
            user = User.query.get(session['user_id'])
            user.name = name
            user.sex = sex
            user.email = email
            user.location = address
            user.about_me = intro
            db.session.add(user)
            db.session.commit()
            return redirect('/myinfos')
    if 'user_id' not in session:    #如果没登录,则跳转到登录页面
        return redirect('/login')
    else:
        user_id = session['user_id']
        atten_user = len(Atten_user.query.filter_by(atten_user_id=user_id).all())  # 我关注了多少个人
        atten_auther = len(Atten_user.query.filter_by(atten_auther=user_id).all())  # 多少个人关注了我
    user = User.query.get(user_id)
    rtime = user.registration_time
    bdays = (datetime.datetime.now() - rtime).days
    byears = math.floor(bdays / 365)
    hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
    timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
    readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行

    return render_template('myinfos.html', user=user, bdays=bdays, byears=byears, params=locals())

@app.route('/checkuname')
def checkuname_views():
    uname = request.args['uname']
    if uname == '':
        return ''
    isExist = db.session.query(User).filter_by(name=uname).first()
    if isExist:
        if isExist.name != uname:
            return '1'
        else:
            return '2'
    else:
        return '0'

@app.route('/logout')
def logout_views():
    if 'username' in session:
        del session['username']
        del session['user_id']
    return redirect('/')

# 个人主页 - 我的发布
@app.route('/mainpage/<user_id>')
def mainpage_views(user_id):
    articlename = request.args.get('articlename', '')
    articles = db.session.query(Article).filter_by(auther=user_id).order_by('article_id desc').all()
    count = db.session.query(Article).filter_by(auther=user_id).count()
    if articlename:
        articles = db.session.query(Article).filter(Article.auther==user_id).filter(Article.title.like('%'+articlename+'%')).all()
        count = db.session.query(Article).filter(Article.auther==user_id).filter(Article.title.like('%'+articlename+'%')).count()
    hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
    timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
    readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
    return render_template('mainpage.html', articles=articles, count=count, user_id=user_id, params=locals())

# 个人主页 - 我的收藏
@app.route('/mainpage-collage/<user_id>')
def mainpagerelease_views(user_id):
    user_info = User.query.filter_by(user_id=user_id).first()
    articles = user_info.collect_articles.all()
    hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
    timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
    readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
    return render_template("mainpage-collage.html", articles=articles, user_id=user_id, params=locals())

# 个人主页 - 我的资源
@app.route('/mainpage-myresource/<user_id>', methods=['GET', 'POST'])
def mainpagemyresource_views(user_id):
    if request.method == 'GET':
        if 'fname' in request.args:
            l = []
            fname = request.args['fname']
            resources = db.session.query(Resource).filter(Resource.fname.like('%'+fname+'%')).filter(Resource.user_id==user_id).all()
            for r in resources:
                l.append(r.to_dict())
            return json.dumps(l)
        resources = db.session.query(Resource).filter_by(user_id=user_id).all()
        hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
        timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
        readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
        return render_template("myresource.html", resources=resources, user_id=user_id,params=locals())
    else:
        resource = Resource()
        f = request.files['file']



        resource.fname = f.filename
        ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        ext = f.filename.split('.')[-1]
        filename = ftime + '.' + ext
        resource.rname = filename
        basedir = os.path.dirname(__file__)
        upload_path = os.path.join(basedir, 'static/upload', filename)


        f.save(upload_path)
        rsize = math.ceil(os.path.getsize(upload_path) / 1024)
        resource.rsize = rsize
        resource.up_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        resource.user_id = session['user_id']
        db.session.add(resource)
        db.session.commit()

        return redirect('/mainpage-myresource/%s' % user_id)

@app.route('/del-resource')
def del_resource_views():
    rid = request.args['rid']
    print(rid)
    resource = Resource.query.filter_by(rid=rid).first()
    db.session.delete(resource)
    db.session.commit()
    return redirect('/mainpage-myresource/%s' % session['user_id'])


@app.route('/mainpage-video/<user_id>', methods=['GET', 'POST'])
def myvideo_views(user_id):
    if request.method == 'GET':
        pageSize = 6
        page = int(request.args.get('page', '1'))
        videos = db.session.query(Video).filter(Video.user_id==user_id).order_by("vid desc").offset((page-1)*pageSize).limit(pageSize).all()
        totalCount = db.session.query(Video).filter(Video.user_id==user_id).count()
        lastpage = math.ceil(totalCount / pageSize)
        prePage = 1
        if page > 1:
            prePage = page - 1
        nextPage = lastpage
        if page < lastpage:
            nextPage = page + 1
        hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
        timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
        readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行
        return render_template('myvideo.html', params=locals(), user_id=user_id)
    else:
        print(1)
        video = Video()
        f = request.files['video']
        vtitle = request.form['vtitle']
        vcontent = request.form['vcontent']
        ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        ext = f.filename.split('.')[-1]
        filename = ftime + '.' + ext
        basedir = os.path.dirname(__file__)
        upload_path = os.path.join(basedir, 'static/upload', filename)
        f.save(upload_path)
        video.user_id = session['user_id']
        video.savename = filename
        video.vtitle = vtitle
        video.vcontent = vcontent
        video.up_date = datetime.date.today()
        db.session.add(video)
        db.session.commit()

        return redirect('/mainpage-video/%s' % user_id)

@app.route('/mainpage-message/<user_id>',methods=['GET','POST'])
def mainpagemessage_views(user_id):
    '''个人中心留言板'''
    if request.method == 'GET':
        messages = db.session.query(Message).filter(Message.messager_other==user_id).order_by(db.desc(Message.message_time)).all()
        list_message = []
        for message in messages:
            dic_message = {}
            user = User.query.filter_by(user_id=message.messager).first()
            username = user.username
            photo = user.photo
            user_id = user.user_id
            dic_message['id'] = message.id  #发到前端标记属于哪个回复框
            dic_message['user_id'] = user_id   #留言者
            print(message.messager)
            dic_message['username']=username
            dic_message['photo'] = photo
            dic_message['message_time']=message.message_time
            dic_message['message_content'] = message.message_content
            list_message.append(dic_message)

        hotcomm = Article.query.order_by(db.desc(Article.like_number)).limit(6).all()  # 点赞排行
        timecomm = Article.query.order_by(db.desc(Article.publish_time)).limit(12).all()  # 时间排序
        readcomm = Article.query.order_by(db.desc(Article.read_quantity)).limit(12).all()  # 阅读量排行


        return render_template("mainpage-message.html", messages=list_message, user_id=user_id, params=locals())
    else:
        id_kuang = request.form.get('id')  #dict_messdata={"id":id,"messdata":messdate}
        messdata = request.form.get('messdata')     #回复数据
        mess = Message.query.filter_by(id=id_kuang).first()
        mess_user = mess.messager   #回复用户

        print(mess_user, messdata)
        mess_insert = Message()
        mess_insert.messager = session['user_id']
        mess_insert.messager_other = mess_user
        mess_insert.message_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mess_insert.message_content = messdata
        db.session.add(mess_insert)
        db.session.commit()

        return '回复成功'




########################搜索模块
@app.route('/home-page', methods=['GET','POST'])
def home_page():
    return render_template('home-page.html')

@app.route('/lbxy_search', methods=['GET','POST'])
def lbxy_search():
    return render_template('lbxy_search.html')

 # 搜索建议处理函数
@app.route('/01-search')
def search_suggest():
  l = []
  keyword=request.args.get('keyword','')
  if keyword != '':
    #去Article表中做模糊查询 - like
    res=db.session.query(Article.title).filter(Article.title.like('%'+keyword+'%')).all()
    #处理结果
    #users = [('wangwc',),('rap wang',)]
    for re in res:
      l.append(re[0])
  jsonStr = json.dumps(l)
  return jsonStr

#搜索内容函数.分页功能
@app.route('/02-search',methods=['POST','GET'])
def search_content():
  l=[]
  pageSize = 5
  page = request.args.get('page','1')
  page = int(page)
  ost = (page-1)*pageSize
  keyword = request.form['keyword']
  print(keyword)

  if keyword != '':
    res = db.session.query(Article.title).filter(Article.title.like('%' + keyword + '%')).all()
    print(res)
    res_all = db.session.query(Article.title).all()
    print(res_all)
    for re in res_all:
      if re not in res:
        res.append(re)
    for re in res:
      l.append(re[0])
    l = l[ost:(ost+5)]
    totalCount = len(l)
    lastPage = math.ceil(totalCount / pageSize)

    print(l)
    prePage = 1
    if page > 1:
      prevPage = page - 1

    # 变量nextPage用于表示下一页的页码
    nextPage = lastPage
    if page < lastPage:
      nextPage = page + 1

    return render_template('lbxy_search_after.html',params=locals())
  else:
    return '搜索内容不能为空'






############################图片上传显示

@app.route('/imageshow/<user_id>',methods=['GET','POST'])
def imageshow(user_id):
    if request.method == 'GET':
        images_lists = ImagesUpload.query.filter_by(uploader=user_id).all()
        user = User.query.filter_by(user_id=user_id).first()

        return render_template('/imageshow/image_index.html', params=locals())


@app.route('/imageupload',methods=['GET', 'POST'])
def imageupload():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/login')
        user_id = session['user_id']
        return render_template('/imageshow/imageupload.html',user_id=user_id)

    else:
        user_id = session['user_id']
        imagebrief = request.form.get('brief')
        imagetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file = request.files['image']
        if not file:
            return '上传空文件'
        try:
            ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            ext = file.filename.split('.')[-1]
            filename = ftime + '.' + ext
            basedir = os.path.dirname(__file__)
            upload_path = os.path.join(basedir, 'static/imgupload', filename)
            file.save(upload_path)
        except Exception as e:
            print('上传失败', e)
            return '上传失败'

        imgupload = ImagesUpload()
        imgupload.uploader = user_id
        imgupload.imagename = filename
        imgupload.imagebrief = imagebrief
        imgupload.imagetime = imagetime
        db.session.add(imgupload)
        db.session.commit()

        return render_template('/imageshow/imageupload.html',user_id=user_id)

if __name__ == "__main__":
    app.run()
