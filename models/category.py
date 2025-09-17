from . import db,u

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    products = db.relationship('Products', secondary='category_and_product', back_populates='categories')

