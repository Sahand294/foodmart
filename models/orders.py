from . import db,u
import datetime
class Orders(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    users_email = db.Column(db.String(100),db.ForeignKey('users.email'))
    purchase_date = db.Column(db.Date, default=datetime.date.today)
    totall_price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(50))
    payment_method = db.Column(db.String(50))
    address = db.Column(db.String(999))
    # address = db.Column(db.Integer,db.ForeignKey('address_user.id'))
    items = db.relationship(
        'Order_items',
        backref='order',
        cascade='all, delete-orphan'
    )

class Order_items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    cart_id = db.Column(db.Integer,db.ForeignKey('carts.id'))
    amount = db.Column(db.Integer)
    price = db.Column(db.Integer)
