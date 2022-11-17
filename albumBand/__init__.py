from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '089ede1b5ebaebb10fa0f3328afb3864'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from albumBand import routes
