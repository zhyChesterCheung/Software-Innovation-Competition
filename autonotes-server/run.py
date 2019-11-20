import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from config import config
from app import db
from app.api import blueprint as api_bp
# from app.APIVX import blueprint as APIVX_bp

app = Flask(__name__)
app.config.from_object(config[os.getenv("FLASK_CONFIG") or 'development'])
app.wsgi_app = ProxyFix(app.wsgi_app)
db.init_app(app)
app.register_blueprint(api_bp)
# app.register_blueprint(APIVX_bp)
