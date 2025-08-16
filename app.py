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
from models.cart import Carts,CartProducts
import os
from models.products import Products
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
app.secret_key = '123'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/install', methods=['GET', 'POST'])
def install():
    global app
    i = SiteSetting.query.filter_by(key="installed").first()
    installed = string_to_bool(i.Value)
    DF_P(app)
    Add_Connection(app)

    if installed:
        return redirect(url_for('home'))


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
        session['websitename'] = Connect.get_value('Name')
        return redirect(url_for('home'))

    return render_template('foodmart1/install.html')








@app.route('/cart',methods=['GET','POST'])
def carts():
    global user
    P_amount = str(session['productamount'])
    logged = session['logged']
    cartid = Carts.query.filter_by(name=session['username']).first()
    cart_items = CartProducts.query.filter_by(cartid=int(cartid.id)).all()
    product_ids = [item.productid for item in cart_items]
    products = []
    for i in product_ids:
        x = Products.query.filter_by(id=int(i)).first()
        amounts = CartProducts.query.filter_by(productid=int(x.id)).first()
        amount = amounts.amount
        products.append([x, amount])
    websitename = Connect.get_value('Name')
    user = ''
    if 'username' in session and session['logged']:
            user = session['username']
    if request.method == 'POST':
        if request.form.get("remove1") == "remove1":
            print('removed')
            productid = request.form.get("id")
            product = Products.query.filter_by(id=int(productid)).first()
            product.stock += 1
            session['productamount'] -= 1
            cartitem = CartProducts.query.filter_by(productid=productid).first()
            if int(cartitem.amount) == 1:
                db.session.delete(cartitem)
            else:
                cartitem.amount -= 1
            db.session.commit()
        if request.form.get("remove") == "remove":
            productid = request.form.get("id")
            product = Products.query.filter_by(id=int(productid)).first()
            quantity = int(request.form.get('amount'))
            product.stock += quantity
            session['productamount'] -= quantity
            cartitem = CartProducts.query.filter_by(productid=productid).first()
            db.session.delete(cartitem)
            db.session.commit()


















    P_amount = str(session['productamount'])
    logged = session['logged']
    cartid = Carts.query.filter_by(name=session['username']).first()
    cart_items = CartProducts.query.filter_by(cartid=int(cartid.id)).all()
    product_ids = [item.productid for item in cart_items]
    products = []
    for i in product_ids:
        x = Products.query.filter_by(id=int(i)).first()
        amounts = CartProducts.query.filter_by(productid=int(x.id)).first()
        amount = amounts.amount
        products.append([x,amount])
        print(x.price,amount)
    return render_template('foodmart1/cartproducts.html',name=websitename,username=user,logged=logged,productamount=P_amount,products=products)













@app.route('/add_to_cart',methods=['GET','POST'])
def add_to_cart():
    if request.method == 'POST':
        print(int(request.form['id']))
        product = Products.query.filter_by(id=int(request.form['id'])).first()
        if product:
            print(product)
        else:
            print('nuh uh')
        cart =     Carts.query.filter_by(name=session['username']).first()
        cart_product = CartProducts.query.filter_by(cartid=int(cart.id),productid=int(product.id)).first()
        if cart_product:
            cart_product.amount += 1
            product.stock -= 1
            db.session.commit()
        else:
            print()
            relation = CartProducts(cartid=int(cart.id),productid=int(product.id),amount=1)
            product.stock -= 1
            db.session.add(relation)
            db.session.commit()
        session['productamount'] += 1
        print(session['productamount'])
    return(redirect(url_for('home')))
@app.route('/',methods=['GET','POST'])
def home():
    if 'logged' not in session:
        session['logged'] = False
    if 'productamount' not in session:
        session['productamount'] = 0

    global user
    websitename = Connect.get_value('Name')
    user = ''
    if 'username' in session and session['logged']:
            user = session['username']
    if request.method == 'POST':
        if request.form.get("action") == "logout":
            session['logged'] = False
            session['productamount'] = 0
            del session['username']
            del session['password']
    amount = str(session['productamount'])
    logged = session['logged']
    print(logged,user)
    return render_template('foodmart1/main2.html',name=websitename,username=user,logged=logged,productamount=amount)




@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    global name, user
    if 'websitename' in session:
        name=session['websitename']
    if 'username' in session:
        user=session['username']
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
    logged = session['logged']
    return render_template('foodmart1/contact-us.html',name=name,username=user,logged=logged)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('starting')
    if request.method == 'POST':
        print('alright doing good')
        password = request.form['password']
        username = request.form['username']
        print('lol')
        user = Users.query.filter_by(username=username).first()
        print('finding account')
        if user:
            if check_password_hash(user.password,password):
                print('password is right')
                session['username'] = request.form['username']
                session['password'] = request.form['password']
                session['logged'] = True
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


@app.route('/about_us',methods=['GET','POST'])
def about_us():
    global name,user
    if 'websitename' in session:
        websitename=session['websitename']
    if 'username' in session:
        user=session['username']
    logged = session['logged']
    return render_template('foodmart1/about_us.html',name=websitename,username=user,logged=logged)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print('making account')
    mistakes = []
    if request.method == 'POST':
        pass
        # print("fff")
        # session['firstname'] = request.form['firstname']
        # session['lastname'] = request.form['lastname']
        # session['email'] = request.form['email']
        # session['username'] = request.form['username']
        # session['password'] = request.form['password']

        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')



        if not is_real_email(email):
            mistakes.append("Email is Wrong")

        # if not errors:
        #     print('must signup')
        AddAccounts.add(email,firstname,lastname,username,password)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('foodmart1/signin.html',errors=mistakes)


@app.errorhandler(401)
def error401():
    return render_template('foodmart1/error.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    DF(app)
    app.run(debug=True)
