from . import db,u
class Orders(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cart = db.Column(db.Integer,db.ForeignKey('carts.id'))
    purchase_date = db.Column(db.Data)