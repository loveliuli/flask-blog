# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:27:56
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-06-19 10:34:57
#表单工具

from flask_wtf import Form, RecaptchaField
from wtforms import StringField, TextField,TextAreaField, PasswordField, BooleanField,widgets
from wtforms.validators import DataRequired, Length, EqualTo, URL


from webapp.models import User


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class CommentForm(Form):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password',validators= [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True

class PostForm(Form):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Content', [DataRequired()])

class RegisterForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])
    #recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        # Is the username already being used
        if user:
            self.username.errors.append("User with that name already exists")
            return False

        return True
