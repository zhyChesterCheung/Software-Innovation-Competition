from . import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    id = db.Column(db.String(16), primary_key=True)
    username = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readble attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id}).decode()

    @staticmethod
    def get_by_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
