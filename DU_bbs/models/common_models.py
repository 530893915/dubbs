#coding:utf8

from exts import db
import datetime
import json
from models.basemodels import BaseModel


# 板块表
class BoardModel(db.Model,BaseModel):
    __tablename__ = 'board'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('cms_user.id'))

    author = db.relationship('CMSUser', backref='boards')

    def to_dict(self):
        model_dict = super(BoardModel,self).to_dict()
        model_dict['post_count'] = self.posts.count()
        return model_dict

# 加精
class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

# 评论
class CommentModel(db.Model):
    __tablename__='comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_removed = db.Column(db.Boolean,default=False)

    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    origin_comment_id = db.Column(db.Integer,db.ForeignKey('comment.id'))

    author = db.relationship('FrontUser',backref='comments')
    post = db.relationship('PostModel',backref='comments')
    origin_comment = db.relationship('CommentModel',backref='replys',remote_side=[id])

# 帖子
class PostModel(db.Model,BaseModel):
    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)
    read_count = db.Column(db.Integer,default=0)
    is_removed = db.Column(db.Boolean,default=False)

    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    highlight_id = db.Column(db.Integer,db.ForeignKey('highlight_post.id'))

    board = db.relationship('BoardModel',backref=db.backref('posts',lazy='dynamic'))
    author = db.relationship('FrontUser',backref='posts')
    highlight = db.relationship('HighlightPostModel',backref='post',uselist=False)

    def to_dict(self):
        model_dict = super(PostModel, self).to_dict()
        model_dict['author'] = self.author.to_dict()
        return model_dict



# 点赞
class PostStarModel(db.Model):
    __tablename__ = 'post_star'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    author = db.relationship('FrontUser',backref='stars')
    post = db.relationship('PostModel',backref='stars')