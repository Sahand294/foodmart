from . import db,u
import datetime
class Orders(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cart = db.Column(db.Integer,db.ForeignKey('carts.id'))
    purchase_date = db.Column(db.Date, default=datetime.date.today)