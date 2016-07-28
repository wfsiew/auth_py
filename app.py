from flask import Flask, request, redirect, url_for, render_template, jsonify, session
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
from flask_mail import Message
from logging.handlers import RotatingFileHandler, SMTPHandler
from config import app, mail
import requests, logging, traceback

login_manager = LoginManager()
login_manager.init_app(app)

class User(object):

    def __init__(self):
        self.email = None
        self.authenticated = False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.email)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '{0}-{1}'.format(self.email, self.is_authenticated())

class Google(object):
    url = 'http://localhost:8000/google/callback/' if app.debug else 'https://apps.redtone.com:8585/oauth/google/callback/'

@login_manager.user_loader
def user_loader(user_id):
    o = User()
    o.email = user_id
    return o

@app.route('/google/callback/')
def callback():
    try:
        code = request.args.get('code')
        url = 'https://accounts.google.com/o/oauth2/token'
        k = {
            'code': code,
            'client_id': '579168859503.apps.googleusercontent.com',
            'client_secret': 'G-WYqCt2UGYZRKq3V4o10wli',
            'redirect_uri': Google.url,
            'grant_type': 'authorization_code'
        }
        r = requests.post(url, data=k)
        d = r.json()

        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        k = {
            'access_token': d.get('access_token')
        }
        r = requests.get(url, params=k)
        m = r.json()
        session['profile'] = m

        user = User()
        user.email = m['email']
        user.authenticated = True
        login_user(user)
        app.logger.info(user)
        return redirect(url_for('profile'))

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return unicode(e)

@app.route('/profile')
def profile():
    try:
        raise Exception('profile')
        g = session['profile']
        return jsonify(g)

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return unicode(e)

@app.route('/login')
def login():
    try:
        user = User()
        user.email = "wingfei.siew@redtone.com"
        user.authenticated = True
        login_user(user)
        app.logger.debug(user)
        return redirect(url_for('index'))

    except Exception as e:
        return unicode(e)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))

@app.route('/')
@login_required
def index():
    return 'ok'

@app.route('/home')
def home():
    google = ('https://accounts.google.com/o/oauth2/auth'
              '?response_type=code'
              '&client_id=579168859503.apps.googleusercontent.com'
              '&redirect_uri={0}'
              '&scope=openid%20profile%20email'
              '&login_hint=email'
              '&approval_prompt=force').format(Google.url)
    return render_template('home.html', url=google)

@app.route('/mail')
def sendmail():
    msg = Message("Hello",
                  sender="redtonernd@redtone.com",
                  recipients=["siewwingfei@hotmail.com"])
    msg.body = render_template('mail.html', name='ben')
    msg.html = render_template('mail.html', name='ben')
    mail.send(msg)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)