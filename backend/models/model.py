from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load

db = SQLAlchemy()

# Class name should be the name of the table
class Users(db.Model):
    username = db.Column(db.String(150), primary_key=True)
    password = db.Column(db.String(150))
    fav_list = db.relationship('Favorites', cascade="all,delete", backref='Users', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

# Still needs to be tested
class Favorites(db.Model):
    fav_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), db.ForeignKey('users.username'))
    restaurant_name = db.Column(db.String(150))

    def __init__(self, fav_id, username, restaurant_name):
        self.fav_id = fav_id
        self.username = username
        self.restaurant_name = restaurant_name

    def __repr__(self):
        return '<Favorites %r>' % self.fav_id


###################### SCHEMAS #########################
class UserSchema(Schema):
    username = fields.Str()
    password = fields.Str()

        # Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class FavoritesSchema(Schema):
    fav_id = fields.Int(dump_only=True)
    username = fields.Nested(UserSchema, validate=must_not_be_blank)
    restaurant_name = fields.Str(required=True, validate=must_not_be_blank)
