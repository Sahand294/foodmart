from . import db,u

class BrandCategory(db.Model):
    __tablename__ = 'brand_categorys'
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(300))
