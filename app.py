from flask import Flask, render_template, session, url_for, request, redirect, flash, Blueprint
from flask_migrate import Migrate
from config import Config
from sending_emails import Send
import re
import dns.resolver
from add_account import AddAccounts
from default_values import DF, Add_Values
from models import db
from models.sitesetting import SiteSetting
from default_connection import Connect
from default_permissions import DF_P,Add_Connection
from models import Users
from werkzeug.security import generate_password_hash,check_password_hash
def is_real_email(email):
    # Step 1: Validate format
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.fullmatch(pattern, email):
        return False

    # Step 2: Check MX records
    domain = email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return False

def string_to_bool(value):
    if isinstance(value,bool):
        return value
    if isinstance(value,str):
        if value.lower() in ['true','True','1']:
            return  True
    return False
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "123"
db.init_app(app)
migrate = Migrate(app, db)

logged = False

@app.route('/install', methods=['GET', 'POST'])
def install():
    global app
    i = SiteSetting.query.filter_by(key="installed").first()
    installed = string_to_bool(i.Value)
    DF_P(app)
    Add_Connection(app)
    if installed:
        return redirect(url_for('home'))

    DF(app)


    if request.method == 'POST':



        name = request.form['Name']

        logo = request.files['Logo']

        template = request.form['Template']

        receiver = request.form['receiver']

        smtp_user = request.form['smtp_user']

        smtp_port = request.form['smtp_port']

        smtp_server = request.form['smtp_server']

        smtp_pass = request.form['smtp_pass']

        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        Add_Values(logo,name, smtp_user, receiver, template, 'True',
                smtp_port, smtp_server, smtp_pass,username,password,firstname,lastname,email)
        return redirect(url_for('home'))

    return render_template('foodmart1/install.html')



@app.route('/')
def home():
    global logged
    name = Connect.get_value('Name')
    user = ''
    if 'username' in session:
        if logged:
            user = session['username']
    elif 'username' in session:
        del session['username']
        del session['password']
    return render_template('foodmart1/main2.html',name=name,username=user,logged=logged)


# @app.route('/index')
# def index():
#     return 'hello'
# @app.route('/login')
# def login():
#     return 'hi'
contact_bp = Blueprint('contact', __name__)


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):
            flash('All fields are required.', 'error')
            return redirect(url_for('contact_us'))

        subject = f"New message from {name}"
        body = f"From: {name} <{email}>\n\n{message}"

        try:
            Send.send_mail(subject, email, body)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message: {str(e)}', 'error')

        return redirect(url_for('contact_us'))

    # GET request - just render the contact form
    return render_template('foodmart1/contact-us.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged
    print('starting')
    if 'username' in session:
        del session['username']
        del session['password']
    if request.method == 'POST':
        print('alright doing good')
        password = request.form['password']
        print('lol')
        user = Users.query.filter_by(username=session['username']).first()
        print('finding account')
        if user:
            if check_password_hash(user.password,password):
                print('password is right')
                session['username'] = request.form['username']
                session['password'] = request.form['password']
                logged = True
                return redirect(url_for('home'))
            else:
                return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))
    return render_template('foodmart1/login.html')


@app.route('/admin', methods=['GET', 'POST'])
def Admin():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']


@app.route('/about_us')
def about_us():
    return render_template('foodmart1/about_us.html')


@app.route('/signup', methods=['GET', 'POST'])
def signin():
    print('making account')
    global logged
    if 'username' in session:
        del session['username']
        del session['password']
    if request.method == 'POST':

        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        # if is_real_email(session['email']):
        #     pass
        # else:
        #
        #     return redirect(url_for('error'))
        logged = True
        email = session['email']
        username = session['username']
        password = session['password']
        firstname = session['firstname']
        lastname = session['lastname']

        # AddAccounts.add(email, firstname, lastname, username, password)
        return redirect(url_for('home'))
    return render_template('foodmart1/signin.html')


@app.errorhandler(401)
def error():
    return render_template('foodmart1/error.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
