from . import db,u

class NormallCategory(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

