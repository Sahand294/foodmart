from models.users import Roles
from models import db
from models.sitesetting import SiteSetting
# from app import app
from werkzeug.utils import secure_filename
import os
from default_connection import Connect
def DF(app):


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
        smtp_server =   SiteSetting.query.filter_by(key="server").first()
        smtp_pass =     SiteSetting.query.filter_by(key="smtp_pass").first()



        if not l:
            l = SiteSetting(key='Logo')
            db.session.add(l)
            db.session.commit()
        if not n:
            n = SiteSetting(key='Name')
            db.session.add(n)
            db.session.commit()
        if not installed:
            installed = SiteSetting(key='installed',Value='False')
            db.session.add(installed)
            db.session.commit()

        if not smtp_port:
            port = SiteSetting(key="smtp_port",Value='587')
            db.session.add(port)
            db.session.commit()

        if not smtp_server:
            server = SiteSetting(key='server',Value='smtp.gmail.com')
            db.session.add(server)
            db.session.commit()

        if not smtp_pass:
            passs = SiteSetting(key='smtp_pass')
            db.session.add(passs)
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
def Add_Values(Logo,Name,user,reciever,T,Installed,smtp_po,smtp_s,smtp_pa):
    logo = SiteSetting.query.filter_by(key="Logo").first()
    name = SiteSetting.query.filter_by(key="Name").first()
    smtp_user = SiteSetting.query.filter_by(key="smtp_user").first()
    receiver_email = SiteSetting.query.filter_by(key="receiver_email").first()
    template = SiteSetting.query.filter_by(key="Template").first()
    installed = SiteSetting.query.filter_by(key="installed").first()
    smtp_port = SiteSetting.query.filter_by(key="smtp_port").first()
    smtp_server = SiteSetting.query.filter_by(key="server").first()
    smtp_pass = SiteSetting.query.filter_by(key="smtp_pass").first()
    if Logo.filename == '':
        pass
    else:
        filename = secure_filename(Logo.filename)
        upload_files = "uploads"
        os.makedirs(upload_files,exist_ok=True)
        filepath = os.path.join(upload_files,filename)
        Logo.save(filepath)
        if logo:
            logo.Value = filepath
            db.session.commit()

    if name:
        print('name')
        name.Value = Name
        db.session.commit()

    if smtp_user:
        smtp_user.Value = user
        db.session.commit()
    if receiver_email:
        print('email')
        receiver_email.Value = reciever
        db.session.commit()
    if template:
        template.Value = T
        db.session.commit()
    if installed:
        installed.Value = Installed
        db.session.commit()
    if smtp_port:
        print('port')
        smtp_port.Value = smtp_po
        db.session.commit()

    if smtp_pass:
        print('pass')
        smtp_pass.Value = smtp_pa
        db.session.commit()
    if smtp_server:
        smtp_server.Value = smtp_s
        db.session.commit()
