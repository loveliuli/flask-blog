from flask import Flask
from models import db
import os
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, UserNeed, RoleNeed
from webapp.models import db,User,Role,Post,Comment,Tag
from controllers.blog import blog_blueprint
from controllers.main import main_blueprint
from webapp.extensions import bcrypt, login_manager, principals, rest_api,celery,debug_toolbar,cache,admin
from webapp.controllers.rest.post import PostApi,CommentApi
from webapp.controllers.rest.auth import AuthApi
#from webapp.tasks import on_reminder_save
from webapp.controllers.admin import (
        CustomView,
        CustomModelView,
        CustomFileAdmin,
        PostView

    )

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    #db.init_app(app)
    #event.listen(Reminder, 'after_insert', on_reminder_save)


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    celery.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)
    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))

    models = [User,Role,Comment,Tag]
    for model in models:
        admin.add_view(CustomModelView(model,db.session,category='Models'))

    admin.add_view(
        PostView(
            Post, db.session, category='PostManager'
        )
    )
    admin.add_view(
        CustomFileAdmin(
            os.path.join(os.path.dirname(__file__), 'static'),
            '/static/',
            name='Static Files'
        )
    )

    rest_api.add_resource(
        AuthApi,
        '/api/auth',
    )
    rest_api.add_resource(
        PostApi,
        '/api/post',
        '/api/post/<int:post_id>',
    )
    rest_api.add_resource(
        CommentApi,
        '/api/comment',
        '/api/comment/<int:comment_id>',
        '/api/post/<int:post_id>/comment',
        '/api/post/<int:post_id>/comment/<int:comment_id>',
    )
    rest_api.init_app(app)



    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user
        print "In __init_.py......:%s" %current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
            print UserNeed(current_user.id)

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
                print RoleNeed(role.name)



    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app('project.config.ProdConfig')
    app.run()
