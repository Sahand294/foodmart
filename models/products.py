from . import db,u
import datetime
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True)
    color = db.Column(db.String(100),nullable=True)
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    name = db.Column(db.String(200))
    brand_id = db.Column(db.Integer,db.ForeignKey('brands.id'))
    brand_name = db.Column(db.String(300),db.ForeignKey('brands.name'))
    about = db.Column(db.String(1000))

class SpecailProducts(db.Model):
    __tablename__ = 'Specailproducts'
    id = db.Column(db.Integer,primary_key=True)
    discount = db.Column(db.Integer)
    start_date = db.Column(db.Date, default=datetime.date.today)
    end_date = db.Column(db.Date, default=datetime.date.today)
    product = db.Column(db.Integer,db.ForeignKey('products.id'))

class CalTaxes:
    def cal(self,price):
        return price * 0.15

class Attribute(db.Model):
    __tablename__ = 'attributes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
class ProductAttribute(db.Model):
    __tablename__ = 'product_attributes'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    attribute_id = db.Column(db.Integer,db.ForeignKey('attributes.id'))
    value = db.Column(db.String(200),nullable=False)
    attribute = db.relationship('Attribute')