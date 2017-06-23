import datetime
from celery.schedules import crontab

class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    RECAPTCHA_PUBLIC_KEY = "6LdY-RkUAAAAAJmnaYfLWuoWaFe-S97ES28mCHA2"
    RECAPTCHA_PRIVATE_KEY = '6LdY-RkUAAAAAC_9-pCchurb-GkYcu-4BOC-3K3X'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class DevConfig(Config):
    SERVER_NAME='42.62.120.210:5000'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    #CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "redis://localhost:6379/0"
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_IMPORTS=("webapp.tasks")
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_PASSWORD = ''
    CACHE_REDIS_DB = '0'
    ''' 
    CELERYBEAT_SCHEDULE = {
        'log-every-30-seconds':{
        'task':'webapp.tasks.digest',
        'schedule':datetime.timedelta(seconds=10),

        },

    }
    '''
    CELERYBEAT_SCHEDULE = {
        'weekly-digest':{
            'task':'webapp.tasks.digest',
            'schedule':crontab(day_of_week=2,hour='23',minute='7')
        },
    }
