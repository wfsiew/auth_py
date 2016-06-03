from flask import Flask
from logging.handlers import RotatingFileHandler, SMTPHandler
from admin.views import admin
from management.views import management
import logging

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(management, url_prefix='/management')

class Config(object):
    DEBUG = False
    SECRET_KEY = 'wfsiew_app'
    SESSION_COOKIE_NAME = 'app_session'
    SESSION_COOKIE_PATH = '/'
    THREADS_PER_PAGE = 2

class ProductionConfig(Config):
    SESSION_COOKIE_PATH = '/app'

class DevelopmentConfig(Config):
    DEBUG = True

app.config.from_object(DevelopmentConfig)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s")
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

ADMINS = ['wingfei.siew@redtone.com']
if not app.debug:
    mailhandler = SMTPHandler('mail.redtone.com', 'redtonernd@redtone.com', ADMINS, 'app ERROR')
    mailhandler.setLevel(logging.ERROR)
    app.logger.addHandler(mailhandler)