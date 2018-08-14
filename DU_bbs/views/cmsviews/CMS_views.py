#coding:utf8

from flask import Blueprint
from flask.views import MethodView
from models.CMS_models import CMSUser,CMSRole
from models.front_models import FrontUser
from models.common_models import BoardModel,PostModel,HighlightPostModel,CommentModel
import flask
from exts import db
from forms.CMS_forms import CMSLoginForm,CMSResetpwdForm,CMSResetmailForm,CMSAddUserForm,CMSBlackListForm,CMSBlackFrontUserForm,CMSEditBoardForm,CMSHighlightPostForm
import constants
from decorators.cmsdecorators import login_required,superadmin_required
from models.modelhelpers import PostModelHelper
from utils import xtjson,xtcache,xtmail
from utils.captcha.xtcaptcha import Captcha
from tasks import celery_send_mail

bp = Blueprint('cms',__name__,subdomain='cms')



# CMS主页视图函数
@bp.route('/')
@login_required
def index():
    return flask.render_template('cms/cms_index.html')

# CMS登录的类视图函数
class CMSLoginView(MethodView):
    def get(self,message=None):
        return flask.render_template('cms/login.html',message=message)

    def post(self):
        form = CMSLoginForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                # 判断当前用户是否被拉黑，如果被拉黑，跳转到没有权限的提示页面
                if not user.is_active:
                    return flask.abort(401)
                flask.session[constants.CMS_SESSION_ID] = user.id
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('cms.index'))
            else:
                return self.get(message = u'邮箱或密码有误！')
        else:
            message = form.get_error()
            return self.get(message=message)


bp.add_url_rule('/login/',view_func=CMSLoginView.as_view('login'))

# CMS用户注销
@bp.route('/logout/')
@login_required
def logout():
    flask.session.pop(constants.CMS_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))

# CMS-个人中心-个人信息
@bp.route('/profile/')
@login_required
def profile():
    return flask.render_template('cms/cms_profile.html')

# CMS-个人中心-修改密码
@bp.route('/resetpwd/',methods=['GET','POST'])
@login_required
def resetpwd():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetpwd.html')
    else:
        form = CMSResetpwdForm(flask.request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            if flask.g.cms_user.check_password(oldpwd):
                flask.g.cms_user.password = newpwd
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error('密码错误！')
        else:
            return xtjson.json_params_error(message=form.get_error())

# CMS-个人中心-修改邮箱
@bp.route('/resetmail/',methods=['GET','POST'])
@login_required
def resetmail():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetmail.html')
    else:
        form = CMSResetmailForm(flask.request.form)
        if form.validate():
            email =form.email.data
            if flask.g.cms_user.email == email:
                return xtjson.json_params_error(message='不能与旧邮箱一致！')
            flask.g.cms_user.email = email
            db.session.commit()
            return xtjson.json_result()
        else:

            return xtjson.json_params_error(message=form.get_error())

# CMS-个人中心-修改邮箱-验证码
@bp.route('/mail_captcha/')
def mail_captcha():

    # 生成验证码

    email = flask.request.args.get('email')

    if xtcache.get(email):
        return xtjson.json_params_error('该邮箱已经发送验证码了！')

    captcha =Captcha.gene_text()

    # 给请求修改邮箱的用户发送邮箱验证码

    # if xtmail.send_mail(subject='DUDU论坛邮箱验证码', receivers=email, body='邮箱验证码：'+captcha):
    #     # 1.为了下次可以验证邮箱和验证码
    #     # 2.为了防止用户不断的刷这个接口
    #     xtcache.set(email,captcha)
    #     return xtjson.json_result()
    # else:
    #     return xtjson.json_server_error()

    celery_send_mail.delay(subject='DUDU论坛邮箱验证码', receivers=email, body='邮箱验证码：'+captcha)
    return xtjson.json_result()

# CMS-CMS用户管理
@bp.route('/cmsusers/')
@login_required
def cmsusers():
    users = CMSUser.query.all()
    context ={
        'users': users
    }
    return flask.render_template('cms/cms_cmsusers.html',**context)

# CMS-CMS用户管理-添加管理员
@bp.route('/add_cmsuser/',methods = ['GET','POST'])
@login_required
def add_cmsuser():
    if flask.request.method == 'GET':
        roles = CMSRole.query.all()
        context = {
            'roles':roles
        }
        return flask.render_template('cms/cms_addcmsuser.html',**context)
    else:
        form = CMSAddUserForm(flask.request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            roles = flask.request.form.getlist('roles[]')
            if not roles:
                return xtjson.json_params_error(message='必须选择至少一个分组！')
            user = CMSUser(email=email,username=username,password=password)
            for role_id in roles:
                role = CMSRole.query.get(role_id)
                role.users.append(user)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())

# CMS-CMS用户管理-编辑
@bp.route('/edit_cmsuser/',methods=['GET','POST'])
@login_required
@superadmin_required
def edit_cmsuser():
    # ?user_id=XXX
    if flask.request.method == 'GET':
        user_id = flask.request.args.get('user_id')
        if not user_id:
            flask.abort(404)
        user = CMSUser.query.get(user_id)
        roles =CMSRole.query.all()
        current_roles = [role.id for role in user.roles]
        context = {
            'user':user,
            'roles':roles,
            'current_roles': current_roles # 存储当前用户所有的角色id
        }
        return flask.render_template('cms/cms_editcmsuser.html',**context)
    else:
        user_id = flask.request.form.get('user_id')
        roles = flask.request.form.getlist('roles[]')
        if not user_id:
            return xtjson.json_params_error(message='没有指定用户ID！')
        if not roles:
            return xtjson.json_params_error(message='必须指定一个用户组！')

        user = CMSUser.query.get(user_id)
        # 清掉之前的角色信息
        user.roles[:] = []
        # 添加新的角色
        for role_id in roles:
            role_model = CMSRole.query.get(role_id)
            user.roles.append(role_model)
        db.session.commit()
        return xtjson.json_result()

# CMS-CMS用户管理-编辑-加入/移出黑名单
@bp.route('/black_list/',methods=['POST'])
@login_required
@superadmin_required
def black_list():
    form = CMSBlackListForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        if user_id == flask.g.cms_user.id:
            return xtjson.json_params_error(message='不能拉黑自己！')
        is_black = form.is_black.data
        user = CMSUser.query.get(user_id)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# CMS-用户管理
@bp.route('/front_users/')
@login_required
def front_users():
    sort = flask.request.args.get('sort')
    # 1：按加入时间排序
    # 2：按发表帖子数量排序
    # 3：按评论数量排序
    front_users = None
    # 如果没有sort，默认按时间排序
    if not sort or sort == '1':
        front_users = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    else:
        front_users = FrontUser.query.all()

    context = {
        'front_users': front_users,
        'current_sort':sort
    }
    return flask.render_template('cms/cms_frontusers.html',**context)

# CMS-用户管理-编辑
@bp.route('/edit_frontuser/')
@login_required
def edit_frontuser():
    user_id = flask.request.args.get('id')
    if not user_id:
        flask.abort(404)

    user = FrontUser.query.get(user_id)
    if not user:
        flask.abort(404)
    return flask.render_template('cms/cms_editfrontuser.html',current_user=user)

# CMS-用户管理-编辑-拉入/移出黑名单
@bp.route('/black_front_user/',methods=['POST'])
@login_required
def black_front_user():
    form = CMSBlackFrontUserForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        is_black = form.is_black.data
        user = FrontUser.query.get(user_id)
        if not user:
            flask.abort(404)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

# CMS-板块管理
@bp.route('/boards/')
@login_required
def boards():
    all_boards = BoardModel.query.all()
    context = {
        'boards':all_boards
    }
    return flask.render_template('cms/cms_boards.html',**context)

# CMS-板块管理-添加板块
@bp.route('/add_board/',methods=['POST'])
@login_required
def add_board():
    name = flask.request.form.get('name')
    # 判断是否输入板块名称
    if not name:
        return xtjson.json_params_error(message='必须指定板块的名称！')

    # 判断板块名称是否重复(在数据库中是否存在)
    board = BoardModel.query.filter_by(name=name).first()
    if board:
        return xtjson.json_params_error(message='该板块已经存在！')

    # 创建板块模型
    board = BoardModel(name=name)
    board.author = flask.g.cms_user
    db.session.add(board)
    db.session.commit()
    return xtjson.json_result()

# CMS-板块管理-编辑
@bp.route('/edit_board/',methods=['POST'])
@login_required
def edit_board():
    form = CMSEditBoardForm(flask.request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        board.name = name
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

# CMS-板块管理-删除
@bp.route('/delete_board/',methods=['POST'])
@login_required
def delete_board():
    board_id = flask.request.form.get('board_id')
    if not board_id:
        return xtjson.json_params_error(message='没有指定板块ID！')

    board = BoardModel.query.filter_by(id=board_id).first()
    if not board:
        return xtjson.json_params_error(message='该板块不存在！请刷新当前页面！')

    # 判断当前板块下帖子数是否大于0，若大于0则不能删除
    # if boards.posts.count() > 0:
    #     return xtjson.json_params_error(message='当前板块帖子数量大于0！')
    db.session.delete(board)
    db.session.commit()
    return xtjson.json_result()

# CMS-帖子管理
@bp.route('/posts/')
@login_required
def posts():
    # 查询字符串
    sort_type = flask.request.args.get('sort',1,type=int)
    board_id = flask.request.args.get('board',0,type=int)
    page = flask.request.args.get('page',1,type=int)
    context = PostModelHelper.post_list(page,sort_type,board_id)
    return flask.render_template('cms/cms_posts.html',**context)



# CMS-帖子管理-加精
@bp.route('/highlight/',methods=['POST'])
def highlight():
    form = CMSHighlightPostForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_hightlight = form.is_highlight.data
        post_model = PostModel.query.get(post_id)
        if is_hightlight:
            if post_model.highlight:
                return xtjson.json_params_error(message='加精失败！该帖子已经加过精了！')
            highlight_model = HighlightPostModel()
            post_model.highlight = highlight_model
            db.session.commit()
            return xtjson.json_result()
        else:
            if not post_model.highlight:
                return xtjson.json_params_error(message='该帖子没有加精！')
            db.session.delete(post_model.highlight)
            db.session.commit()
            return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

# CMS-帖子管理-移除
@bp.route('/remove_post/',methods=['POST'])
@login_required
def remove_post():
    post_id = flask.request.form.get('post_id')
    if not post_id:
        return xtjson.json_params_error(message='必须输入帖子ID！')
    post_model = PostModel.query.get(post_id)
    post_model.is_removed = True
    db.session.commit()
    return xtjson.json_result()

# 其他函数

# 钩子函数，返回一个字典，可在模板上下文中使用
@bp.context_processor
def cms_context_processor():
    id = flask.session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        return {'cms_user':user}
    else:
        return {}

# 钩子函数,在视图函数执行之前执行，通过session获取当前用户信息
@bp.before_request
def cms_before_request():
    id = flask.session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        flask.g.cms_user = user


# 401错误函数
@bp.errorhandler(401)
def cms_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.render_template('cms/cms_401.html'),401

# 404错误函数
@bp.errorhandler(404)
def cms_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return flask.render_template('cms/cms_404.html'),404
