from . import db,u
class Orders(db.model):
    id = db.Column(db.Integer,primarykey=True)
    cart = db.Column(db.Integer,db.Foriegnkey('carts.id'))
    purchase_date = db.Column(db.Data)