from . import db,u
import datetime
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(100),nullable=False)
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    name = db.Column(db.String(200))
    about = db.Column(db.String(1000))
    cart_products = db.relationship('CartProducts', back_populates="product")
    categories = db.relationship('Category', secondary='category_and_product', back_populates='products')
    product_stripe_id = db.Column(db.String(200))
    product_price_stripe_id = db.Column(db.String(200))


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