from . import db,u

class BrandCategory(db.model):
    __tablename__ = 'brand-categorys'
    id = db.Column(db.Integer,primarykey=True)
    name= db.Column(db.String(300))
