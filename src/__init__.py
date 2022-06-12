from email.policy import default
from enum import unique
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

app= Flask(__name__)

connection_token = stripe.terminal.ConnectionToken.create()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'not very secret now'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_tR3PYbcVNZZ796tH88S4VQ2u'

stripe.api_key = app.config['STRIPES_SECRET_KEY']

db = SQLAlchemy(app)

bcrypt  = Bcrypt(app)

loginmanager = LoginManager(app)

class Item(db.Model): # identifier needed to create models
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(),nullable=False)
    category = db.Column(db.String(length=20),nullable=False,unique=True)
    description = db.Column(db.String(length=120),nullable=False,unique=True)
    barcode = db.Column(db.String(length=12),nullable=False,unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id') )


    def __repr__(self):
        return f'Item {self.name}'

    def sell(self,user):
        self.owner = None
        user.coins += self.price
        db.session.commit()
    
    def buy(self,obj):
        self.owner = obj.id
        obj.coins-=self.price
        db.session.commit()


class User(db.Model,UserMixin): #UserMixin adds attributes that flask_login needs (isauth,isactive,.etc)
    id = db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=20),nullable=False,unique=True)
    email=db.Column(db.String(),unique=True,nullable=False)
    # set default value
    coins=db.Column(db.Integer(),default=30000,nullable=False)
    #hash passw
    passh=db.Column(db.String(60),nullable=False)
    sold=db.relationship('Item',backref='owned_used',lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, plain_text_password):
        print(plain_text_password)
        self.passh = generate_password_hash(plain_text_password)

    def check_password_correction(self, attempted_password):
        print(self.passh + "pashh")
        return check_password_hash(self.passh, attempted_password)

    def can_purch(self,obj):
        return self.coins > obj.price

    def can_sell(self,obj):
        return obj in self.sold 

    def __repr__(self):
        return f'User {self.name}'



from src import routes 

