from . import db
from models.products import Products
# cart_products = db.Table(
#     'cart_products',
#     db.Column('Cart_id',db.Integer,db.ForeignKey('carts.id')),
#     db.Column('Product_id', db.Integer, db.ForeignKey('products.id'))
# )
class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey('users.id'),unique=True)
    users = db.relationship('Users', back_populates='cart', lazy=True)
    cart_products = db.relationship('CartProducts', back_populates="cart")
class CartProducts(db.Model):
    __tablename__ = 'cart_products'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cartid = db.Column(db.Integer,db.ForeignKey('carts.id'))
    productid = db.Column(db.Integer,db.ForeignKey('products.id'))
    amount = db.Column(db.Integer)
    cart = db.relationship("Carts", back_populates="cart_products")
    product = db.relationship("Products", back_populates="cart_products")