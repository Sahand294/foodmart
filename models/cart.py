from . import db
from models.products import Products
class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100))

class CartProducts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer)
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    cart_id = db.Column(db.Integer,db.ForeignKey('carts.id'))