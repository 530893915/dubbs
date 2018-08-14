#coding: utf8


from redis import StrictRedis
import json


class PostRedist(object):

    def __init__(self,redis):
        self.__redis = redis

    def add_post(self,post_model):
        # redis.set
        # lpush/rpush
        # lpop/rpop
        # string/list/set/sorted set/hash
        self.__redis.lpush('topest_post', post_model.to_json())

    def posts(self,start, end):
        """
        获取所有帖子
        """
        return self.__redis.lrange('topest_post', start=start, end=end)

class BoardRedis(object):

    def __init__(self,redis):
        self.__redis = redis

    def add_board(self,board_model):
        self.__redis.lpush('boards', board_model.to_json())

    def boards(self,start,end):
        all_boards = self.__redis.lrange('boards',start,end)
        board_dicts = []
        for board_json in all_boards:
            board_dicts.append(json.loads(board_json.decode('utf-8')))
        return board_dicts

# 对redis的封装
class BBSRedis(object):
    __redis = StrictRedis(host='39.108.222.5', port=6379, password='Qq199678')

    # BBSRedis.post
    post = PostRedist(__redis)
    board = BoardRedis(__redis)

    @classmethod
    def get(cls,key):
        return cls.__redis.get(key)

    @classmethod
    def set(cls,key,value,timeout):
        cls.__redis.set(key,value,timeout)
