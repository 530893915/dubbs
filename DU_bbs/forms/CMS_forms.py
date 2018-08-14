#coding:utf8

from forms.Base_forms import BaseForm
from wtforms import StringField,BooleanField,ValidationError,IntegerField
from wtforms.validators import InputRequired,Email,Length,EqualTo
from utils import xtcache
from models.common_models import BoardModel



# CMS-登录验证
class CMSLoginForm(BaseForm):
    email = StringField(validators=[InputRequired(message='邮箱不能为空！'),Email(message='必须为邮箱格式！')])
    password = StringField(validators=[InputRequired(message='密码不能为空！'),Length(6,20,message='密码长度必须在6-20个字符之间！')])
    remember = BooleanField()

#CMS-个人中心-修改密码验证
class CMSResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message='旧密码不能为空！'),Length(6,20)])
    newpwd = StringField(validators=[InputRequired(message='新密码不能为空！'),Length(6,20)])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd',message='两次密码必须一致！')])

# CMS-个人中心-修改邮箱
class CMSResetmailForm(BaseForm):
    email = StringField(validators=[InputRequired(message='必须输入邮箱！'),Email(message='请输入正确的邮箱格式！')])
    captcha = StringField(validators=[InputRequired(message='必须输入验证码！'),Length(4,4)])

    # 验证用户输入的验证码和发送的验证码是否一致
    def validate_captcha(self,field):
        email = self.email.data
        captcha = field.data
        captcha_cache = xtcache.get(email)
        if not captcha_cache or captcha_cache.lower() != captcha:
            raise ValidationError(message='验证码错误！')
        return True

# CMS-CMS用户管理-添加管理员-验证
class CMSAddUserForm(BaseForm):
    email = StringField(validators=[InputRequired(message='邮箱不能为空！'),Email(message='请输入正确的邮箱格式！')])
    username = StringField(validators=[InputRequired(message='用户名不能为空！')])
    password = StringField(validators=[InputRequired(message='密码不能为空！'),Length(6,20,message='密码长度必须在6-20个字符之间！')])

# CMS-CMS用户管理-编辑-加入/移出黑名单
class CMSBlackListForm(BaseForm):
    user_id = IntegerField(validators=[InputRequired(message='必须传入ID！')])
    is_black = IntegerField(validators=[InputRequired(message='必须指定是否加入黑名单！')])

# CMS-用户管理-编辑-拉入/移出黑名单
class CMSBlackFrontUserForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message='必须传入ID！')])
    is_black = IntegerField(validators=[InputRequired(message='必须指定是否加入黑名单！')])

# CMS-板块管理-编辑
class CMSEditBoardForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message='必须传入板块ID！')])
    name = StringField(validators=[InputRequired(message='必须输入板块名称！')])

    def validate_board_id(self,field):
        board_id = field.data
        board = BoardModel.query.filter_by(id=board_id).first()
        if not board:
            raise ValidationError(message='该板块不存在！')
        return True

    def validate_name(self,field):
        name = field.data
        board = BoardModel.query.filter_by(name=name).first()
        if board:
            raise ValidationError(message='请不要输入相同的名称！')
        return True

# CMS-帖子管理-加精
class CMSHighlightPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message='必须传入帖子ID！')])
    is_highlight = BooleanField(validators=[InputRequired(message='必须输入行为！')])