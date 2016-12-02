# -*- coding: utf-8 -*-
import redis
# from rediscluster import StrictRedisCluster
# r = redis.StrictRedis(host='192.168.23.133',port=6379)
def nexusCA ():
#     sql = ''
#     nexus_config_info = database.sql_statement(sql)
#     r.set('guo','shuai')
#     nexus_url =r.get('nexus_url')

    nexus_login = {'nexus_url':'http://192.168.23.133:9002/nexus','nexus_password':'admin123','nexus_user':'admin'}
    return nexus_login
def nexusConfig():
    nexus_server_config = {''}
    return nexus_server_config