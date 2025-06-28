from . import db,u

class CategoryAndProduct(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    categoryid = db.Column(db.Integer,db.ForeignKey('category.id'))
    productid = db.Column(db.Integer,db.ForeignKey('products.id'))