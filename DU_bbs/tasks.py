#coding:utf8

from celery import Celery
from utils import xtmail
from flask import Flask
import config


app = Flask(__name__)
app.config.from_object(config)


celery = Celery('sbbs_taks',
             broker='redis://:Qq199678@39.108.222.5:6379/0',
             backend='redis://:Qq199678@39.108.222.5:6379/0')

@celery.task
def celery_send_mail(subject,receivers,body=None,html=None):
    with app.app_context():
        xtmail.send_mail(subject,receivers,body,html)
