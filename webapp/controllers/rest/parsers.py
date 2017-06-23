# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-04-05 17:59:00
# @Last Modified by:   liuli
# @Last Modified time: 2017-04-09 10:31:20
#获取url中的参数

from flask.ext.restful import reqparse

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument('page', type=int, location=['args', 'headers'])
post_get_parser.add_argument('user', type=str, location=['args', 'headers'])

post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to edit posts"
)
post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help="Title is required"
)
post_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help="Body text is required"
)
post_post_parser.add_argument(
    'tags',
    type=str,
    action='append'
)

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)


post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
post_put_parser.add_argument(
    'title',
    type=str
)
post_put_parser.add_argument(
    'text',
    type=str
)
post_put_parser.add_argument(
    'tags',
    type=str
)

post_delete_parser = reqparse.RequestParser()
post_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to delete posts"
)


comment_put_parser = reqparse.RequestParser()
comment_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
comment_put_parser.add_argument(
    'text',
    type=str
)

comment_post_parser = reqparse.RequestParser()
comment_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
comment_post_parser.add_argument(
    'text',
    type=str
)
comment_post_parser.add_argument(
    'name',
    type=str
)
comment_get_parser = reqparse.RequestParser()
comment_get_parser.add_argument('page', type=int, location=['args', 'headers'])
comment_get_parser.add_argument('post_id', type=int, location=['args', 'headers'])

comment_delete_parser = reqparse.RequestParser()
comment_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to delete posts"
)

