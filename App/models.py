from flask_login import UserMixin
from App import db



class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True) 

    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    ## reset token for reset password
    reset_token = db.Column(db.String(100))
    reset_token_expiry = db.Column(db.DateTime)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    product = db.relationship('Product', backref='user', lazy=True, cascade="all, delete-orphan")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) 

    tangram_id = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
