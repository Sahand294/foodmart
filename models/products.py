from . import db,u

class Products(db.model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primarykey=True)
    color = db.Column(db.String(100),nullable=True)
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)
    name = db.Column(db.String(200))
    brand_id = db.Column(db.Integer,db.Foriegnkey('brands.id'))
    brand_name = db.Column(db.String(300),db.Foriegnkey('brands.name'))
    about = db.Column(db.String(1000))

class SpecailProducts(db.model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primarykey=True)
    discount = db.Column(db.Integer)
    start_date = db.Column(db.Data)
    end_date = db.Column(db.Data)
    product = db.Column(db.Integer,db.Foriegnkey('products.id'))

class CalTaxes:
    def cal(self,price):
        return price * 0.15

class Attribute(db.model):
    __tablename__ = 'attributes'
    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
class ProductAttribute(db.model):
    __tablename__ = 'product_attributes'
    id = db.Column(db.Integer, primarykey=True)
    product_id = db.Column(db.Integer,db.Foriegnkey('products.id'))
    attribute_id = db.Column(db.Integer,db.Foriegnkey('attributes.id'))
    value = db.Column(db.String(200),nullable=False)
    attribute = db.relationship('attributes')