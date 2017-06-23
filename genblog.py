#!/usr/bin/env Python
#encoding:utf-8
import random
import datetime
from webapp.models import db, User, Post, Tag
from webapp import create_app

app=create_app('webapp.config.ProdConfig')
#获取ID为1的用户
#生成4类标签和标签列表
user=User.query.get(1)
tag_one = Tag('Python')
tag_two = Tag('Flask')
tag_three = Tag('SQLAlechemy')
tag_four = Tag('Jinjia')
tag_list = [tag_one,tag_two,tag_three,tag_four]

s='Example text'

#Post为提交的标题
for i in xrange(100):
    new_post = Post("Post"+str(i))
    new_post.user = user
    new_post.publish_date = datetime.datetime.now()
    new_post.text = s
    new_post.tags = random.sample(tag_list, random.randint(1,3))
    db.session.add(new_post)
db.session.commit()
