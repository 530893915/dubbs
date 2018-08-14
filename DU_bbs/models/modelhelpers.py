#coding:utf8

# 这个文件用来给模型添加方法

import constants
from exts import db
from models.common_models import PostModel, HighlightPostModel, CommentModel, PostStarModel, BoardModel
from datetime import datetime
import json
from utils.xtredis import BBSRedis

class PostModelHelper(object):

    class PostSortType(object):
        CREATE_TIME = 1
        HIGHLIGHT_TIME = 2
        COMMENT_COUNT = 3
        STAR_COUNT = 4

    # redis优化后
    @classmethod
    def post_list_cached(cls,page,sort_type,board_id):
        start = (page - 1) * constants.PAGE_NUM
        end = start + constants.PAGE_NUM

        # sort_type = 1 :按时间排序
        # sort_type = 2 :按加精排序
        # sort_type = 3 :按评论量排序
        # sort_type = 4 :按点赞量排序

        # if sort_type == cls.PostSortType.CREATE_TIME:
        #     posts = PostModel.query.filter(PostModel.is_removed == False).order_by(PostModel.create_time.desc())
        # elif sort_type == cls.PostSortType.HIGHLIGHT_TIME:
        #     posts = db.session.query(PostModel).outerjoin(HighlightPostModel).filter(
        #         PostModel.is_removed == False).order_by(HighlightPostModel.create_time.desc(),
        #                                                 PostModel.create_time.desc())
        # elif sort_type == cls.PostSortType.COMMENT_COUNT:
        #     posts = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
        #         db.func.count(CommentModel.id).desc(), PostModel.create_time.desc())
        # elif sort_type == cls.PostSortType.STAR_COUNT:
        #     posts = db.session.query(PostModel).outerjoin(PostStarModel).group_by(PostModel.id).order_by(
        #         db.func.count(PostStarModel.id).desc(), PostModel.create_time.desc())
        # else:
        #     posts = PostModel.query.order_by(PostModel.create_time.desc())

        # if board_id:
        #     posts = posts.filter(PostModel.board_id == board_id)



        # 分页
        posts = BBSRedis.post.posts(start,end)
        post_dict_list = []
        for post_json in posts:
            post_dict = json.loads(post_json.decode('utf-8'))
            post_dict_list.append(post_dict)
        posts = post_dict_list

        first_post = posts[0]
        print(first_post)
        total_post_count = int(BBSRedis.get(constants.TOTAL_POST_COUNT_KEY))
        total_page = total_post_count // constants.PAGE_NUM
        if total_post_count % constants.PAGE_NUM > 0:
            total_page += 1

        pages = []
        # 往前找，不能小于1
        tmp_page = page - 1
        while tmp_page >= 1:
            if tmp_page % 5 == 0:
                break
            pages.append(tmp_page)
            tmp_page -= 1

        # 往后面找，不能大于总共的页数
        tmp_page = page
        while tmp_page <= total_page:
            if tmp_page % 5 == 0:
                pages.append(tmp_page)
                break
            else:
                pages.append(tmp_page)
                tmp_page += 1

        pages.sort()

        context = {
            'posts': posts,
            'boards': BBSRedis.board.boards(0,-1),
            'pages': pages,
            'c_page': page,
            't_page': total_page,
            'c_sort': sort_type,
            'c_board': board_id
        }

        return context