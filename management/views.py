from flask import render_template, Blueprint

management = Blueprint('management', __name__, template_folder='templates')

@management.route('/')
def index():
	return render_template('management/index.html')