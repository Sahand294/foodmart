from . import db,u

class Country(db.model):
    __tablename__ = 'country'
    id = db.Column(db.Integer,primarykey=True)
    name = db.Column(db.String(30))
    key = db.Column(db.String(200),Unique=True)

class City(db.model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(30))
    key = db.Column(db.String(200),Unique=True)
    province = db.Column(db.Integer,db.Foriegnkey('provinces.id'))

class ProvinceOrTerritories(db.model):
    __tablename__ = 'provinces'
    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(200))
    country = db.Column(db.Integer,db.Foriegnkey('country.id'))

class Address_User(db.model):
    __tablename__ = 'address_user'
    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(30))
    city = db.Column(db.Integer,db.Foriegnkey('city.id'))
    address = db.Column(db.String(999))
    postal_code = db.Column(db.String(999))
    User = db.Column(db.Integer,db.Foriegnkey('users.id'))