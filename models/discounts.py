from . import db,u
class Coupons(db.model):
    id =  db.Column(db.Integer,primarykey=True)
    amount = db.Column(db.Integer)
