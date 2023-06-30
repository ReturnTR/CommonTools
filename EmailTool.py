#coding:utf-8
import sys
import traceback
import yaml
import atexit
import time 

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from .YamlTool import get_ymal
from .TimeTool import Timer

# 自定义配置信息，用变量的方式

# 邮件配置文件
email_config_file="CommonTools/email_info_template.yaml"

# 异常信息标题
error_title="程序异常退出"

# 程序结束标题
exit_title="程序结束"

# 程序结束内容
exit_content=""

# 详细信息记录文件
email_log_file=[]

# 记录时间
timer=Timer()


# 邮件发送函数
class SendEmail:

    def __init__(self,filename):
        self.email_info=get_ymal(filename)
        #初始化邮件配置信息
        message = MIMEMultipart()
        #设置主题
        message['Subject'] = self.email_info["subject"]
        #设置发送用户
        message['From'] = self.email_info["send_user_name"]+"<"+self.email_info["send_user"]+">"
        #设置接收用户
        message['To'] = ";".join(self.email_info["receive_user"])
        #设置抄送
        if self.email_info["copy_user"]:message["Cc"]= ";".join(self.email_info["copy_user"])
        #设置附件
        for attach_file in self.email_info["attach_file"]:
            # 构造附件
            attach_file_str = MIMEApplication(open(attach_file, 'rb').read())
            attach_file_str.add_header('Content-Disposition', 'attachment', filename=attach_file.split("/")[-1])
            # 添加附件到邮件信息当中去
            message.attach(attach_file_str)
        self.message=message

    def set_content(self,content):
        """填写邮件内容"""
        self.email_info["content"]=content

    def set_subject(self,subject):
        """设置主题，即标题"""
        self.message["Subject"]=subject

    def add_file(self,filename):
        """添加文件，可多次添加"""
        attach_file_str = MIMEApplication(open(filename, 'rb',encoding='utf-8').read())
        attach_file_str.add_header('Content-Disposition', 'attachment', filename=filename.split("/")[-1])
        self.message.attach(attach_file_str)

    def send(self):
        #注册内容
        if not self.email_info["content"]:print("没有填写邮件内容！");exit()
        self.message.attach(MIMEText(self.email_info["content"], _subtype='plain', _charset='utf-8'))
        #服务连接
        server=smtplib.SMTP()
        server.connect(self.email_info["email_host"])
        #邮件登录
        server.login(self.email_info["send_user"],self.email_info["password"])
        #发送邮件内容
        server.sendmail(self.message["From"],self.email_info["receive_user"],self.message.as_string())
        #关掉连接
        server.close()



# 注册程序正常退出下的信息
def exithook():
    if not sys.exc_info()[0]:
        sen=SendEmail(email_config_file)
        sen.set_subject(exit_title)
        sen.set_content(timer.check()+exit_content)
        sen.send()
atexit.register(exithook)

# 注册异常结束下的信息
def excepthook(exc_type, exc_value, exc_traceback):
    exception_info = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    sen=SendEmail(email_config_file)
    sen.set_content(timer.check()+exception_info)
    sen.set_subject(error_title)
    sen.send()
sys.excepthook = excepthook

if __name__ == '__main__':
    content="hehe"
    sen=SendEmail(email_config_file)
    sen.set_content(content)
    sen.send()