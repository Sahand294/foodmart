from . import db,u

class Carts(db.model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer,primarykey=True)
    name= db.Column(db.String(100))

class CartProducts(db.model):
    id = db.Column(db.Integer,primarykey=True)
    amount = db.Column(db.Integer)
    product_id = db.Column(db.Integer,db.Foriegnkey('products.id'))
    cart_id = db.Column(db.Integer,db.Foriegnkey('carts.id'))