# -*- coding:utf-8 -*-

import logging
from flask import session
from . import api
from ihome import db
from ihome import models


@api.route('/')
def hello_world():
    # session['name'] = 'itcast'
    print session.get('_permanent')
    logging.fatal('fatal')
    logging.error('error')
    logging.warn('warn')
    logging.info('info')
    logging.debug('debug')
    return 'Hello Wolrd!'


@api.route('/demo', methods=['GET', 'POST'])
def demo():
    return 'demo'
