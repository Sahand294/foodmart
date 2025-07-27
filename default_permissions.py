from models.users import Roles
from models import db
from models.sitesetting import SiteSetting
# from app import app
from werkzeug.utils import secure_filename
import os
def Add_Values_P():
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