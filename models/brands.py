from . import db,u

class Brands(db.model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer,primarykey=True)
    name = db.Column(db.String(300),unique=True)
    brandcategory = db.Column(db.Integer,db.Foriegnkey('brand-categorys.id'))
