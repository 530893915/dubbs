#coding: utf8

import redis


cache = redis.Redis(host='39.108.222.5', port=6379, password='Qq199678')


#################字符串操作#################
# 设置值
cache.set('read_count',1)
print(cache.lrange('read_count',1,0))
# 获取
# print cache.get('username')
# 删除
# cache.delete('username')
# 增加
# cache.incr('read_count')
# 递减
# cache.decr('read_count')
# print cache.get('read_count')

#################列表操作#################
# cache.lpush('languages','python')
# cache.lpush('languages','php')
# cache.lpush('languages','javascript')
# cache.lpush('languages','lua')
#
# print cache.lrange('languages',0,-1)

#################集合操作#################
# cache.sadd('team','xiaotuo')
# cache.sadd('team','datuo')
# cache.sadd('team','slice')
# cache.sadd('team','awen')
#
# print cache.smembers('team')


#################hash操作#################
# cache.hset('website','baidu','baidu.com')
# cache.hset('website','google','google.com')
#
# print cache.hgetall('website')


pip = cache.pipeline()
pip.set('username','dfsadfsdfasdfsdfsdfds')
pip.set('password','1111111111111')
pip.execute()






