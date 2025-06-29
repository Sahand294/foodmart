from . import db,u

class PaymentMethod(db.Model):
    __tablename__ = 'PaymentMethod'
    authentication = db.Column(db.Text)
    payment_name = db.Column(db.String(100),unique=True)
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.Text)

