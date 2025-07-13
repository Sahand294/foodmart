from flask import Flask,render_template,session,url_for,request,redirect,flash,Blueprint
from flask_migrate import Migrate
from models import db
from config import  Config
from sending_emails import Send
import re
import dns.resolver
from add_account import AddAccounts
from default_values import add_them

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

app = Flask(__name__)
migrate = Migrate(app,db)
app.config.from_object(Config)
app.secret_key = "123"
db.init_app(app)
logged = False
# add_them(app)
@app.route('/')
def home():  # put application's code here
    global logged
    user = ''
    if 'username' in session:
        if logged:
            user = session['username']
    elif 'username' in session:
        del session['username']
        del session['password']
    return render_template('foodmart1/main2.html')
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

@app.route('/login',methods=['GET','POST'])
def login():
    global logged
    if 'username' in session:
        del session['username']
        del session['password']
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        logged = True
        return redirect(url_for('home'))
    return render_template('foodmart1/login.html')
@app.route('/admin',methods=['GET','POST'])
def Admin():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
@app.route('/about_us')
def about_us():
    return render_template('foodmart1/about_us.html')

@app.route('/signup', methods=['GET','POST'])
def signin():
    print('make it')
    global logged
    if 'username' in session:
        del session['username']
        del session['password']
    if request.method == 'POST':
        print('hi')
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if is_real_email(session['email']):
            print('not uh oh')
        else:
            print('uh oh')
            return redirect(url_for('error'))
        # logged = True
        email = session['email']
        username =  session['username']
        password = session['password']
        firstname = session['firstname']
        lastname = session['lastname']
        print('processing')
        AddAccounts.add(email,firstname,lastname,username,password)
        return redirect(url_for('home'))
    return render_template('foodmart1/signin.html')

@app.route('/error401')
def error():
    return render_template('foodmart1/error.html')
if __name__ == '__main__':
    add_them(app)
    with app.app_context():
        db.create_all()

    app.run()
