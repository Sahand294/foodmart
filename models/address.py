from . import db
import datetime

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    key = db.Column(db.String(200), unique=True)

    provinces = db.relationship(
        'ProvinceOrTerritories',
        backref='country_obj',
        cascade='all, delete-orphan'
    )

class ProvinceOrTerritories(db.Model):
    __tablename__ = 'provinces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    country = db.Column(db.Integer, db.ForeignKey('country.id', ondelete='CASCADE'))

    cities = db.relationship(
        'City',
        backref='province_obj',
        cascade='all, delete-orphan'
    )

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    key = db.Column(db.String(200), unique=True)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id', ondelete='CASCADE'))

    addresses = db.relationship(
        'Address_User',
        backref='city_obj',
        cascade='all, delete-orphan'
    )

class Address_User(db.Model):
    __tablename__ = 'address_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id', ondelete='CASCADE'))
    address = db.Column(db.String(999))
    postal_code = db.Column(db.String(999))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))