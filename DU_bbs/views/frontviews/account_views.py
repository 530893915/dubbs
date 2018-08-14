#coding:utf8


# 短信

from utils.aliyunsdk import aliyun
from utils import xtjson
from utils.captcha.xtcaptcha import Captcha
from utils import xtcache
from flask import Blueprint, views
from io import BytesIO as StringIO
import flask
import constants
from forms.front_forms import FrontRegistForm,FrontLoginForm,SettingsForm
from models.front_models import FrontUser
from exts import db
from decorators.frontdecorators import login_required
from datetime import datetime





bp = Blueprint('account',__name__,url_prefix='/account')




@bp.route('/')
def index():
    return 'front user page'



# 前台-注册
class RegistView(views.MethodView):

    def get(self,message=None,**kwargs):
        context = {
            'message':message
        }
        context.update(kwargs)
        return flask.render_template('front/front_regist.html',**context)

    def post(self):
        form = FrontRegistForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return flask.redirect(flask.url_for('post.index'))
        else:
            telephone = flask.request.form.get('telephone')
            username = flask.request.form.get('username')
            # password = flask.request.form.get('password')
            # password_repeat = flask.request.form.get('password_repeat')
            return self.get(message=form.get_error(),telephone=telephone,username=username)

bp.add_url_rule('/regist/', view_func=RegistView.as_view('regist'))

# 前台-登录
class LoginView(views.MethodView):

    def get(self,message=None):
        return flask.render_template('front/front_login.html',message=message)

    def post(self):
        form = FrontLoginForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                # 验证成功，做登录操作
                flask.session[constants.FRONT_SESSION_ID] = user.id
                if user.old_login_time:
                    user.last_login_time = user.old_login_time
                user.old_login_time = datetime.now
                if remember:
                    flask.session.permanent = True
                return flask.redirect(flask.url_for('post.index'))
            else:
                return self.get(message='手机号码或密码错误！请重试！')
        else:
            return self.get(message=form.get_error())

bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

# 前台-用户-退出登录
@bp.route('/logout/')
def logout():
    flask.session.pop(constants.FRONT_SESSION_ID)
    return flask.redirect(flask.url_for('account.login'))

# 前台-用户-设置
@bp.route('/settings/',methods=['GET','post'])
@login_required
def settings():
    if flask.request.method == 'GET':
        return flask.render_template('front/front_settings.html')
    else:
        form = SettingsForm(flask.request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data

            user_model = flask.g.front_user
            user_model.username = username
            if realname:
                user_model.realname = realname
            if qq:
                user_model.qq = qq
            if avatar:
                user_model.avatar = avatar
            if signature:
                user_model.signature = signature
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())




# 前台-注册-手机验证码(6位数字)
@bp.route('/sms_captcha/')
def sms_captcha():
    telephone = flask.request.args.get('telephone')
    if not telephone:
        return xtjson.json_params_error(message='必须指定手机号码！')

    if xtcache.get(telephone):
        return xtjson.json_params_error(message='1分钟内请勿重复发送！')

    code = Captcha.gene_text_num()
    # /accoutn/sms_captcha/?telephone=12345678900
    # telephone = flask.request.form.get('telephone')
    result = aliyun.send_sms(telephone,code=code)
    print(result)
    if result:
        xtcache.set(telephone, code)
        return xtjson.json_result()
    else:
        return xtjson.json_server_error()


# 前台-登录/注册-图形验证码
@bp.route('/graph_captcha/')
def graph_captcha():
    text,image = Captcha.gene_code()
    # StringIO相当于是一个管道
    out = StringIO()
    # 把image塞到StingIO这个管道中
    image.save(out,'png')
    # 将StringIO的指针指向开始的位置
    out.seek(0)

    # 生成一个响应对象，out.read是把图片流给读出来
    response = flask.make_response(out.read())
    # 指定响应的类型
    response.content_type = 'image/png'
    xtcache.set(text.lower(),text.lower(),timeout=2*60)
    return response














