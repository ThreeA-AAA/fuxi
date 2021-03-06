#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2019/1/20
# @File    : access_auth.py
# @Desc    : ""

from flask import request
from fuxi.core.databases.orm.auth.user_orm import DBFuxiAdmin
from flask_restful import Resource, reqparse
from fuxi.core.data.response import Response
from fuxi.common.utils.logger import logger
from fuxi.core.auth.token import auth

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('uid', type=int)
parser.add_argument('nick', type=str)
parser.add_argument('email', type=str)


class UserManageV1(Resource):
    @auth
    def post(self):
        try:
            args = parser.parse_args()
            username = args['username']
            password = args['password']
            nick = args['nick']
            email = args['email']
            if DBFuxiAdmin.add_admin(
                username=username, password=password,
                nick=nick, email=email
            ):
                return Response.success(message="add successful")
            else:
                return Response.failed(message="add admin failed", code=10401)
        except Exception as e:
            logger.warning("add admin failed: {}".format(e))
            return Response.failed(message=e)


class TokenManageV1(Resource):
    @staticmethod
    def get():
        try:
            args = parser.parse_args()
            remote_ip = request.remote_addr
            username = args['username']
            password = args['password']
            token = DBFuxiAdmin.get_token(username, password)
            if token:
                logger.success("{} {} authentication success".format(remote_ip, username))
                return Response.success(data=token, message="authentication success")
            else:
                error = "{} authentication failed: {} {}".format(remote_ip, username, password)
                logger.warning(error)
                return Response.failed(message=error, code=10401)
        except Exception as e:
            logger.warning("get token failed: {}".format(e))
            return Response.failed(message=e)

    @staticmethod
    def put():
        try:
            args = parser.parse_args()
            remote_ip = request.remote_addr
            username = args['username']
            password = args['password']
            token = DBFuxiAdmin.refresh_token(username, password)
            if token:
                logger.success("{} {} token refresh success".format(remote_ip, username))
                return Response.success(data=token)
            else:
                error = "{} token refresh failed: {} {}".format(remote_ip, username, password)
                logger.warning(error)
                return Response.failed(message=error, code=10401)
        except Exception as e:
            logger.warning("refresh token failed: {}".format(e))
            return Response.failed(message=e)

