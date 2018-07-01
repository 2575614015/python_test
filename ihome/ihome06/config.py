# -*- coding:utf-8 -*-

import redis

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome06'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''
    import base64, os
    base64.b64encode(os.urandom(24))
    '''
    SECRET_KEY = 'w3qIRx4Myh9Yki9xnzPf3kXLQndHBF6c'

    # 创建redis实例用到的参数
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 配置Flask-Session信息
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True

    # 扩展默认会有redis的地址信息(127.0.0.1, 6379), 以及前缀信息(session)
    SESSION_REDIS = redis.StrictRedis(port=REDIS_PORT, host=REDIS_HOST)
    PERMANENT_SESSION_LIFETIME = 86400 * 2


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome07'
    pass