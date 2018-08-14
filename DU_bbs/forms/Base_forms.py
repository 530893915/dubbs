#coding:utf8
from flask_wtf import FlaskForm

# 用于获取错误信息并返回
class BaseForm(FlaskForm):
    def get_error(self):
        _, values = self.errors.popitem()
        message = values[0]
        return message