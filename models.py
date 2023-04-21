from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    '''
    set user variables and rules for each input to be stored. 
    Then define methods to return set values.
    '''
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True )
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.g_auth_verify = g_auth_verify
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def __repr__(self):
        return f'User {self.email} has been added! Memer on ~'


class Storm(db.Model):
    id = db.Column(db.String, primary_key=True)
    type_storm = db.Column(db.String(10), nullable=True, default='')
    severity = db.Column(db.String(100), nullable=False)
    date_happened = db.Column(db.String(150), nullable=True, default='')
    damage_cost = db.Column(db.String(150), nullable=True, default='')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, type_storm, user_token, id='', severity='', date_happened='', damage_cost=''):
        self.id = self.set_id()
        self.type_storm = type_storm
        self.severity= severity
        self.date_happened = date_happened
        self.damage_cost = damage_cost
        self.user_token = user_token
    
    def __repr__(self):
        return f'Your storm information "{self.title}" has been added'

    def set_id(self):
        return (secrets.token_urlsafe())


class StormSchema(ma.Schema):
    class Meta:
        fields = ['id', 'type_storm', 'severity', 'date_happened', 'damage_cost']

storm_schema = StormSchema()
storms_schema = StormSchema(many=True)