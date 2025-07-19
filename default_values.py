from models.users import Roles
from models import db
from models.sitesetting import SiteSetting
# from app import app

def add_them(app):


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
        e = SiteSetting.query.filter_by(key="smtp_user").first()
        ec = SiteSetting.query.filter_by(key="receiver_email").first()
        t = SiteSetting.query.filter_by(key="Template").first()
        installed =   SiteSetting.query.filter_by(key="installed").first()
        smtp_port = SiteSetting.query.filter_by(key="smtp_port").first()
        smtp_server =   SiteSetting.query.filter_by(key="smtp_server").first()
        smtp_pass =     SiteSetting.query.filter_by(key="smtp_pass").first()



        if not l:
            l = SiteSetting(key='Logo')
            db.session.add(l)
            db.session.commit()
        if not installed:
            installed = SiteSetting(key='installed',value='False')
            db.session.add(installed)
            db.session.commit()

        if not smtp_port:
            port = SiteSetting(key="smtp_port",value='587')
            db.session.add(port)
            db.session.commit()

        if not smtp_server:
            server = SiteSetting(key='server',value='smtp.gmail.com')
            db.session.add(server)
            db.session.commit()

        if not smtp_pass:
            passs = SiteSetting(key='smtp_pass')
            db.session.add(n)
            db.session.commit()

        if not e:
            e = SiteSetting(key='smtp_user')
            db.session.add(e)
            db.session.commit()
        if not ec:
            ec = SiteSetting(key='receiver_email')
            db.session.add(ec)
            db.session.commit()
        if not t:
            t = SiteSetting(key='Template')
            db.session.add(t)
            db.session.commit()
