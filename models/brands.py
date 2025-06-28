from . import db,u

class Brands(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(300),unique=True)
    brandcategory = db.Column(db.Integer,db.ForeignKey('brand-categorys.id'))
