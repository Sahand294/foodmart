from . import db,u
class SiteSetting(db.Model):
    __tablename__ = 'sitesetting'
    id = db.Column(db.Integer,primary_key=True)
    key = db.Column(db.String(30),unique=True)
    Value = db.Column(db.Text)