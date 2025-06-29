from . import db,u
import datetime
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    key = db.Column(db.String(200),unique=True)

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    key = db.Column(db.String(200),unique=True)
    province = db.Column(db.Integer,db.ForeignKey('provinces.id'))

class ProvinceOrTerritories(db.Model):
    __tablename__ = 'provinces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    country = db.Column(db.Integer,db.ForeignKey('country.id'))

class Address_User(db.Model):
    __tablename__ = 'address_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    city = db.Column(db.Integer,db.ForeignKey('city.id'))
    address = db.Column(db.String(999))
    postal_code = db.Column(db.String(999))
    User = db.Column(db.Integer,db.ForeignKey('users.id'))