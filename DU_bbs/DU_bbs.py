#coding:utf8
import flask
from flask import Flask
import config
import constants
from exts import db,mail
from models.front_models import FrontUser
from utils import xtjson
from views.frontviews import post_views,account_views
from views.cmsviews import CMS_views

from flask_wtf import CSRFProtect




app = Flask(__name__)

app.config.from_object(config)

CSRFProtect(app)

mail.init_app(app)

db.init_app(app)

# 注册蓝图
app.register_blueprint(post_views.bp)
app.register_blueprint(account_views.bp)
app.register_blueprint(CMS_views.bp)



@app.before_request
def post_before_request():
    id = flask.session.get(constants.FRONT_SESSION_ID)
    if id:
        user = FrontUser.query.get(id)
        flask.g.front_user = user


@app.context_processor
def post_context_processor():
    if hasattr(flask.g,'front_user'):
        return {'front_user': flask.g.front_user}
    return {}

# 401错误函数
@app.errorhandler(401)
def post_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.redirect(flask.url_for('account.login'))

# 404错误函数
@app.errorhandler(404)
def post_page_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return flask.render_template('front/front_404.html'),404




if __name__ == '__main__':
    app.run(debug=True)
