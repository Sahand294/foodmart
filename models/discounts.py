from . import db,u
class Coupons(db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer)
