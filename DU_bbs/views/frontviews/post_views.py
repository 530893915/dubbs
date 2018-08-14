#coding:utf8

from flask import Blueprint
from models.common_models import BoardModel,PostModel,CommentModel,PostStarModel,HighlightPostModel
import flask
from exts import db
from forms.front_forms import AddPostForm,AddCommentForm,StarPostForm
import constants
from decorators.frontdecorators import login_required
from utils import xtjson,xtredis
import qiniu
from models.modelhelpers import PostModelHelper

bp = Blueprint('post',__name__)

# 前台-主页
@bp.route('/')
def index():
    # posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    # boards = BoardModel.query.all()
    # context = {
    #     'posts':posts,
    #     'boards':boards
    # }
    return post_list(1,1,0)

# 前台-主页-翻页
@bp.route('/list/<int:page>/<int:sort_type>/<int:board_id>/')
def post_list(page,sort_type,board_id):
    # model_json = PostModelHelper.to_json(PostModel.query.first())
    context = PostModelHelper.post_list_cached(page,sort_type,board_id)
    return flask.render_template('front/front_index.html',**context)


# 前台-主页-发表新帖子
@bp.route('/add_post/',methods=['GET','POST'])
@login_required
def add_post():
    if flask.request.method == 'GET':
        boards = BoardModel.query.all()
        return flask.render_template('front/front_addpost.html',boards=boards)
    else:
        form = AddPostForm(flask.request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post_model = PostModel(title=title,content=content)
            board_model = BoardModel.query.filter_by(id=board_id).first()
            if not board_model:
                return xtjson.json_params_error(message='该板块不存在！')
            post_model.board = board_model
            post_model.author = flask.g.front_user
            db.session.add(post_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())

# 前台-帖子详情
@bp.route('/post_detail/<int:post_id>/')
def post_detail(post_id):
    # 路径的形式：/post_detail/1/ 为了SEO的优化
    # 查询字符串的形式：/post_detail/?post_id=1/
    post_model = PostModel.query.filter(PostModel.is_removed==False,PostModel.id==post_id).first()
    if not post_model:
        flask.abort(404)
    post_model.read_count += 1
    db.session.commit()
    star_author_ids = [star_model.author.id for star_model in post_model.stars]
    context = {
        'post':post_model,
        'star_author_ids':star_author_ids
    }
    return flask.render_template('front/front_postdetail.html', **context)

# 前台-帖子详情-发表评论
@bp.route('/add_comment/',methods=['GET','POST'])
@login_required
def add_comment():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('post_id',type=int)
        comment_id = flask.request.args.get('comment_id',type=int)
        context = {
            'post':PostModel.query.get(post_id)
        }
        if comment_id:
            context['origin_comment']=CommentModel.query.get(comment_id)
        return flask.render_template('front/front_addcomment.html',**context)
    else:
        form = AddCommentForm(flask.request.form)
        if form.validate():
            post_id = form.post_id.data
            content = form.content.data
            comment_id = form.comment_id.data

            comment_model = CommentModel(content=content)

            post_model = PostModel.query.get(post_id)
            if comment_id:
                origin_comment = CommentModel.query.get(comment_id)
                comment_model.origin_comment = origin_comment
            comment_model.post = post_model
            comment_model.author = flask.g.front_user

            db.session.add(comment_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())

# 前台-帖子详情-点赞
@bp.route('/star_post/',methods=['POST'])
@login_required
def star_post():
    form = StarPostForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data
        post_model = PostModel.query.get(post_id)
        star_model = PostStarModel.query.filter_by(author_id=flask.g.front_user.id, post_id=post_id).first()
        if is_star:
            if star_model:
                return xtjson.json_params_error(message='您已经点过赞了！')
            star_model = PostStarModel()
            star_model.author = flask.g.front_user
            star_model.post = post_model
            db.session.add(star_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            if star_model:
                db.session.delete(star_model)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message='你还没对该帖子点赞！')


    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('/test/')
def test():
    # posts = PostModel.query.filter(PostModel.is_removed==False).slice(0,50)
    # for post_mode in posts:
    #     xtredis.BBSRedis.post.add_post(post_mode)
    boards = BoardModel.query.all()
    for board_model in boards:
        xtredis.BBSRedis.board.add_board(board_model)

    return 'success'




# 前台-发表新帖子-上传图片或视频（七牛）
@bp.route('/qiniu_token/')
def qiniu_token():
    # 授权
    q = qiniu.Auth(constants.QINIU_ACCESS_KEY, constants.QINIU_SECRET_KEY)

    # 选择七牛的云空间
    bucket_name = 'dubbs'

    # 生成token
    token = q.upload_token(bucket_name)

    return flask.jsonify({'uptoken': token})














