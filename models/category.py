from . import db,u

class NormallCategory(db.model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primarykey=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

