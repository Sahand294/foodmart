from models import Roles
from models import db
from models import Permision
from sqlalchemy.exc import IntegrityError
# from app import app
from werkzeug.utils import secure_filename
import os
def DF_P(app):


    with app.app_context():
        customer = Roles.query.filter_by(name="Customer").first()
        admin = Roles.query.filter_by(name="Admin").first()

        if not customer:
            c = Roles(name='Customer', description='Buys stuff from shop')
            db.session.add(c)
            db.session.commit()
            customer = c  # now customer is not None

        if not admin:
            a = Roles(name='Admin', description='Has access to config, edits the website, and can kick members')
            db.session.add(a)
            db.session.commit()

    with app.app_context():

        view_u = Permision.query.filter_by(name="view users").first()
        delete_u = Permision.query.filter_by(name="delete users").first()
        view_p = Permision.query.filter_by(name="view products").first()
        delete_p = Permision.query.filter_by(name="delete products").first()
        add_p = Permision.query.filter_by(name="add products").first()
        view_c =   Permision.query.filter_by(name="view categorys").first()
        delete_c = Permision.query.filter_by(name="delete categorys").first()
        add_c =   Permision.query.filter_by(name="add categorys").first()
        buy_p =     Permision.query.filter_by(name="buy products").first()



        if not view_u:
            l = Permision(name='view users')
            db.session.add(l)
            db.session.commit()
        if not delete_u:
            n = Permision(name='delete users')
            db.session.add(n)
            db.session.commit()
        if not view_p:
            installed = Permision(name='view products')
            db.session.add(installed)
            db.session.commit()

        if not delete_p:
            port = Permision(name="delete products")
            db.session.add(port)
            db.session.commit()

        if not add_p:
            server = Permision(name='add products')
            db.session.add(server)
            db.session.commit()

        if not view_c:
            passs = Permision(name="view categorys")
            db.session.add(passs)
            db.session.commit()

        if not delete_c:
            e = Permision(name='delete categorys')
            db.session.add(e)
            db.session.commit()
        if not add_c:
            ec = Permision(name='add categorys')
            db.session.add(ec)
            db.session.commit()
        if not buy_p:
            t = Permision(name='buy products')
            db.session.add(t)
            db.session.commit()
def Add_Connection(app):
    with app.app_context():
        customer = Roles.query.filter_by(name="Customer").first()
        admin = Roles.query.filter_by(name="Admin").first()
        view_u = Permision.query.filter_by(name="view users").first()
        delete_u = Permision.query.filter_by(name="delete users").first()
        view_p = Permision.query.filter_by(name="view products").first()
        delete_p = Permision.query.filter_by(name="delete products").first()
        add_p = Permision.query.filter_by(name="add products").first()
        view_c = Permision.query.filter_by(name="view categorys").first()
        delete_c = Permision.query.filter_by(name="delete categorys").first()
        add_c = Permision.query.filter_by(name="add categorys").first()
        buy_p = Permision.query.filter_by(name="buy products").first()
        customer.permissions.extend([view_u,view_p,view_c,buy_p])
        try:
            admin.permissions.extend([view_u,view_p,view_c,buy_p,delete_u,delete_p,add_p,delete_c,add_c])
            db.session.commit()
        except IntegrityError as e:
            pass