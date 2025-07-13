from models.users import Roles
from models import db
from models.sitesetting import SiteSetting
from app import app  # Replace with the actual path to your Flask app instance


def add_them():


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
        l = SiteSetting.query.filter_by(key="Logo").first()
        n = SiteSetting.query.filter_by(key="Name").first()
        e = SiteSetting.query.filter_by(key="Email").first()
        ec = SiteSetting.query.filter_by(key="Email code").first()
        t = SiteSetting.query.filter_by(key="Template").first()

        if not l:
            l = SiteSetting(key='Logo')
            db.session.add(l)
            db.session.commit()
        if not n:
            n = SiteSetting(key='Name')
            db.session.add(n)
            db.session.commit()
        if not e:
            e = SiteSetting(key='Email')
            db.session.add(e)
            db.session.commit()
        if not ec:
            ec = SiteSetting(key='Email code')
            db.session.add(ec)
            db.session.commit()
        if not t:
            t = SiteSetting(key='Template')
            db.session.add(t)
            db.session.commit()
