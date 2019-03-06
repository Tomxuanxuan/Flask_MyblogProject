'''设置发送邮件验证码'''

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class send_mail:
    '''发送邮件'''
    def __init__(self, recv_user, check_code):
        self.recv_user = recv_user  #收件人邮箱
        self.check_code = check_code    #验证码
        self.sender = 'tomxuanxuan@qq.com'   #发件服务器(发件人)
        self.password = 'hxipajvqehzhdjgd'

    def mail(self):
        res = True
        try:
            print(self.sender)
            print(self.password)
            msg = MIMEText('您好,您的注册码为: '+self.check_code+',不要告诉别人哟~', _subtype='plain', _charset='UTF-8') #邮件内容
            msg['From'] = formataddr(['checkmail', self.sender])    #发件人邮箱昵称,邮箱账号
            msg['To'] = formataddr(['checker', self.recv_user]) #收件人邮箱昵称,邮箱账号
            msg['Subject'] = '您的注册确认'   #邮件标题

            server = smtplib.SMTP_SSL('smtp.qq.com', 465)   #发件人 SMTP 服务器
            server.login(self.sender, self.password)    #邮箱账号密码登录
            server.sendmail(self.sender, [self.recv_user, ], msg.as_string())    #发件人邮箱,收件人邮箱,邮件内容
            server.quit()   #关闭连接
            print('邮件发送成功')
        except Exception as e:
            res = False
            print('邮件发送失败:', e)
        return res


