#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import smtplib
import datetime
from email.mime.text import MIMEText
from flask import render_template

from webapp.extensions import celery
from webapp.models import Post

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task()
def log(msgs):
    return msgs

@celery.task()
def multiply(x, y):
    return x * y

@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self, pk):
    reminder = Reminder.query.get(pk)
    msg = MIMEText(reminder.text)

    msg['Subject'] = "hello"
    msg['From'] = "505711559@qq.com"
    msg['To'] = reminder.email

    try:
        smtp_server = smtplib.SMTP('smtp.163.com')
        smtp_server.starttls()
        smtp_server.login('xuequn_2008', 'qianXUN521')
        smtp_server.sendmail("", [reminder.email], msg.as_string())
        smtp_server.close()

        return
    except Exception, e:
        self.retry(exc=e)


@celery.task(
    bind=True,
    ignore_result=False,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    from webapp.models import Post
    # find the start and end of this week
    year, week = datetime.datetime.now().isocalendar()[0:2]
    date = datetime.date(year, 1, 1)
    if (date.weekday() > 3):
        date = date + datetime.timedelta(7 - date.weekday())
    else:
        date = date - datetime.timedelta(date.weekday())
    delta = datetime.timedelta(days=(week - 1) * 7)
    start, end = date + delta, date + delta + datetime.timedelta(days=6)

    posts = Post.query.filter(
        Post.publish_date >= start,
        Post.publish_date <= end
    ).all()
    #return posts
    logger.info('Adding {0}1'.format(self))
    if (len(posts) == 0):
        return
    logger.info('Adding {0}2'.format(self))
    try:
        from flask import render_template
        text = render_template("digest.html",posts=posts)
        logger.info('Adding {0}3'.format(self))
    except Exception as e:
        logger.info('Exception happend!! {0}4'.format(self))
        with open('text.txt','w') as f:
            f.write(str(e))
    msg = MIMEText(text, 'html','utf-8')

    msg['Subject'] = "Weekly Digest"
    msg['From'] = "xuequn_2008@163.com"
    logger.info('Adding {0}5'.format(self))
    try:
        smtp_server = smtplib.SMTP('smtp.163.com')
        smtp_server.starttls()
        smtp_server.login('xuequn_2008', 'qianXUN521')
        smtp_server.sendmail(msg['From'], ["505711559@qq.com"], msg.as_string())
        smtp_server.close()

        return 
    except Exception, e:
        self.retry(exc=e)


def on_reminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id,), eta=self.date)
