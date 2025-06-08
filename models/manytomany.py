from . import db,u

class CategoryAndProduct(db.model):
    id = db.Column(db.Integer,primarykey=True)
    categoryid = db.Column(db.Integer,db.Foriegnkey('category.id'))
    productid = db.Column(db.Integer,db.Foriegnkey('products.id'))