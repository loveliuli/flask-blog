# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-04-05 16:17:42
# @Last Modified by:   liuli
# @Last Modified time: 2017-04-09 11:29:56
#所有API实现

import datetime
from flask import abort
from flask.ext.login import current_user
from flask.ext.restful import Resource, fields, marshal_with
from webapp.controllers.rest.fields import HTMLField

from webapp.models import db, User, Post, Tag,Comment
from webapp.controllers.rest.parsers import (
    post_get_parser,
    post_post_parser,
    post_put_parser,
    post_delete_parser,
    comment_put_parser,
    comment_get_parser,
    comment_delete_parser,
    comment_post_parser
)

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'id': fields.Integer(),
    'author': fields.String(attribute=lambda x: x.user.username),
    'title': fields.String(),
    'text': HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_date': fields.DateTime(dt_format='iso8601')
}

comment_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'text': HTMLField(),
    'date': fields.DateTime(dt_format='iso8601'),
    'post_id': fields.Integer()
}


class CommentApi(Resource):
    @marshal_with(comment_fields)
    def get(self, comment_id=None):
        if comment_id:
            comment = Comment.query.get(comment_id)
            if not comment:
                abort(404)
            return comment
        else:
            args = comment_get_parser.parse_args()
            page = args['page'] or 1
            print 'args is %s' %(args)
            if args['post_id']:
                post = Post.query.filter_by(id=args['post_id']).first()
                if not post:
                    abort(404)
                comments = post.comments.order_by(
                    Comment.date.desc()
                ).paginate(page, 30)
            else:
                comments = Comment.query.order_by(
                    Comment.date.desc()
                ).paginate(page, 30)
            return comments.items

    def post(self, post_id=None,comment_id=None):
        print "In commentPostAPI"
        print "post_id is %s" %post_id
        print "comment_id is %s" %comment_id
        if comment_id or not post_id:
            abort(400)
        else:
            args = comment_post_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            post = Post.query.filter_by(id=post_id).first()
            print "user is %s,post is %s" %(user,post)
            if not user or not post:
                abort(401)
            if user.username == 'admin123':
                new_comment = Comment()
                new_comment.user = args['name']
                new_comment.date = datetime.datetime.now()
                new_comment.text = args['text']
                new_comment.post_id = post_id
            else:
                comment_user = args['name']

                if user.username != comment_user:
                    abort(401)
                new_comment = Comment()
                new_comment.name = user.username
                new_comment.date = datetime.datetime.now()
                new_comment.text = args['text']
                new_comment.post_id = post_id

            db.session.add(new_comment)
            db.session.commit()
            return new_comment.id, 201


    def put(self, comment_id=None,post_id=None):
        print "in CommentApi func"
        print current_user
        if not post_id:
            if not comment_id:
                abort(400)

            comment = Comment.query.get(comment_id)

            if not comment:
                abort(404)

            args = comment_put_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            print user
            if not user:
                abort(401)
            if user != current_user:
                abort(403)
            if args['text']:
                comment.text = args['text']
            comment.date = datetime.datetime.now()
        else:
            comment = Comment.query.get(comment_id)
            post_com=Comment.query.filter_by(post_id=post_id).first()
            if not comment or not post_com:
                abort(404)
            args = comment_put_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)
            if user != current_user:
                abort(403)
            if args['text']:
                comment.text = args['text']
            comment.date = datetime.datetime.now()

        db.session.add(comment)
        db.session.commit()
        return comment.id, 201

    def delete(self, comment_id=None):
        print "in delete func"
        print current_user
        if not comment_id:
            abort(400)

        comment = Comment.query.get(comment_id)
        if not comment:
            abort(404)

        args = comment_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        print user
        if user.username != comment.name:
             abort(401)
        if user.username == 'admin':
            db.session.delete(comment)
            db.session.commit()
            return "", 204

class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)

            return post
        else:
            args = post_get_parser.parse_args()
            page = args['page'] or 1
            print 'args is %s page is %s' %(args,page)
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)

                posts = user.posts.order_by(
                    Post.publish_date.desc()
                ).paginate(page, 30)
            else:
                posts = Post.query.order_by(
                    Post.publish_date.desc()
                ).paginate(page, 30)

            return posts.items

    def post(self, post_id=None):
        if post_id:
            abort(400)
        else:
            args = post_post_parser.parse_args(strict=True)

            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)

            new_post = Post(args['title'])
            new_post.user = user
            new_post.date = datetime.datetime.now()
            new_post.text = args['text']

            if args['tags']:
                print args['tags']
                for item in args['tags']:
                    tag = Tag.query.filter_by(title=item).first()

                    # Add the tag if it exists. If not, make a new tag
                    if tag:
                        new_post.tags.append(tag)
                    else:
                        new_tag = Tag(item)
                        new_post.tags.append(new_tag)

            db.session.add(new_post)
            db.session.commit()
            return new_post.id, 201

    def put(self, post_id=None):
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_put_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if not user:
            abort(401)
        if user != post.user:
            abort(403)

        if args['title']:
            post.title = args['title']

        if args['text']:
            post.text = args['text']

        if args['tags']:
            print args['tags']
            print type(args['tags'])
            #for item in args['tags']:
            tag = Tag.query.filter_by(title=args['tags']).first()

            # Add the tag if it exists. If not, make a new tag
            if tag:
                post.tags.append(tag)
            else:
                new_tag = Tag(args['tags'])
                post.tags.append(new_tag)

        db.session.add(post)
        db.session.commit()
        return post.id, 201

    def delete(self, post_id=None):
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_delete_parser.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])
        if user != post.user:
            abort(401)

        db.session.delete(post)
        db.session.commit()
        return "", 204
