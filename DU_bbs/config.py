#coding:utf8
import os

SECRET_KEY = os.urandom(24)

DB_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/dubbs?charset=utf8'

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = 'dudu.com:5000'


# 邮箱的配置(flask_mail)
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USERNAME = '530893915@qq.com'
MAIL_PASSWORD = 'lwfdsvojgffrbghe'
MAIL_DEFAULT_SENDER = '530893915@qq.com'
MAIL_USE_TLS = True

# MAIL_USE_TLS加密：端口号587
# MAIL_USE_SSL加密：端口号465
# QQ邮箱不支持非加密方式发送邮件
