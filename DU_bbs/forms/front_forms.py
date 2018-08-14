#coding:utf8

from forms.Base_forms import BaseForm
from wtforms import StringField,BooleanField,ValidationError,IntegerField
from wtforms.validators import InputRequired,Email,Length,EqualTo,URL
from utils import xtcache


# 图形验证码验证
class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[InputRequired(message='必须输入图形验证码！')])

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        cache_captcha = xtcache.get(graph_captcha.lower())
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message='图形验证码错误！')
        return True

# 前台-注册表单验证
class FrontRegistForm(GraphCaptchaForm):
    telephone = StringField(validators=[InputRequired(message='手机号码不能为空！'),Length(11,11,message='手机号码格式不正确！')])
    sms_captcha = StringField(validators=[InputRequired(message='短信验证码不能为空！')])
    username = StringField(validators=[InputRequired(message='用户名不能为空！')])
    password = StringField(validators=[InputRequired(message='密码不能为空！'), Length(6, 20, message='密码长度必须在6-20个字符之间！')])
    password_repeat = StringField(validators=[InputRequired(message='必须确认密码！'),EqualTo('password', message='两次密码必须一致！')])
    graph_captcha = StringField(validators=[InputRequired(message='必须输入图形验证码！')])

    # 短信验证码验证
    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        cache_captcha = xtcache.get(telephone)
        if not cache_captcha or cache_captcha.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误！')
        return True



# 前台-登录表单验证
class FrontLoginForm(GraphCaptchaForm):
    telephone = StringField(validators=[InputRequired(message='手机号码不能为空！'), Length(11, 11, message='手机号码格式不正确！')])
    password = StringField(validators=[InputRequired(message='密码不能为空！'), Length(6, 20, message='密码长度必须在6-20个字符之间！')])

    remember = IntegerField()

# 前台-发布新帖子验证
class AddPostForm(GraphCaptchaForm):
    title = StringField(validators=[InputRequired(message='必须输入标题！')])
    board_id = IntegerField(validators=[InputRequired(message='必须传入板块ID！')])
    content = StringField(validators=[InputRequired(message='必须输入内容！')])

# 前台-帖子详情-发表评论验证
class AddCommentForm(BaseForm):
    post_id =IntegerField(validators=[InputRequired(message='必须传入帖子ID！')])
    content = StringField(validators=[InputRequired(message='必须输入评论内容！')])
    comment_id = IntegerField()

# 前台-帖子详情-点赞验证
class StarPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message='必须传入点赞ID！')])
    is_star = BooleanField(validators=[InputRequired(message='必须输入赞的行为！')])

# 前台-用户-设置
class SettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message='必须输入用户名！')])
    realname = StringField(validators=[Length(2,4,message='真实姓名格式错误！')])
    qq = StringField()
    avatar = StringField(validators=[URL(message='头像格式不正确！')])
    signature = StringField()