#coding:utf-8
import sys
import traceback
import yaml
import atexit

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from .YamlTool import get_ymal


# 自定义配置信息，用变量的方式

# 邮件配置文件
email_config_file="CommonTools/email_info_template.yaml"

# 异常信息开头
error_prefix_info="程序异常退出"

# 程序正常结束信息，一般在程序结束后设置
exit_info="程序结束"

# 邮件发送函数
class SendEmail:

    def __init__(self,filename):
        self.email_info=get_ymal(filename)

    def set_content(self,content):
        """填写邮件内容"""
        self.email_info["content"]=content

    def send(self):
        #初始化
        message = MIMEMultipart()
        #设置主题
        message['Subject'] = self.email_info["subject"]
        #设置发送用户
        message['From'] = self.email_info["send_user_name"]+"<"+self.email_info["send_user"]+">"
        #设置接收用户
        message['To'] = ";".join(self.email_info["receive_user"])
        #设置抄送
        if self.email_info["copy_user"]:message["Cc"]= ";".join(self.email_info["copy_user"])
        #设置内容
        if not self.email_info["content"]:print("没有填写邮件内容！");exit()
        message.attach(MIMEText(self.email_info["content"], _subtype='plain', _charset='utf-8'))
        #设置附件
        for attach_file in self.email_info["attach_file"]:
            # 构造附件
            attach_file_str = MIMEApplication(open(attach_file, 'rb').read())
            attach_file_str.add_header('Content-Disposition', 'attachment', filename=attach_file.split("/")[-1])
            # 添加附件到邮件信息当中去
            print(attach_file_str)
            message.attach(attach_file_str)
        #服务连接
        server=smtplib.SMTP()
        server.connect(self.email_info["email_host"])
        #邮件登录
        server.login(self.email_info["send_user"],self.email_info["password"])
        #发送邮件内容
        server.sendmail(message["From"],self.email_info["receive_user"],message.as_string())
        #关掉连接
        server.close()

def send_email(content):
    sen=SendEmail(email_config_file)
    sen.set_content(content)
    sen.send()

# 注册程序正常退出下的信息
def exithook():
    send_email(exit_info)
atexit.register(exithook)

# 注册异常结束下的信息
def excepthook(exc_type, exc_value, exc_traceback):
    exception_info=error_prefix_info+"\n"
    exception_info += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    send_email(exception_info)
sys.excepthook = excepthook

if __name__ == '__main__':
    send_email("email_info_template.yaml","hehehhe")