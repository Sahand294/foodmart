from flask import Flask, render_template, session, url_for, request, redirect, flash, Blueprint, jsonify, \
    render_template_string
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
from models import Users,Roles
from models.cart import Carts,CartProducts
import stripe
from models.manytomany import CategoryAndProduct
from models.category import Category
from models.products import Products
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# it is up to date!
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
@app.route('/admin_products',methods=["POST","GET"])
def admin_products():
    if request.method == "POST":
        if request.form.get('remove1') == "remove1":
            id = int(request.form['id'])
            p = Products.query.filter_by(id=id).first()
            relation = CategoryAndProduct.query.filter_by(productid=p.id).first()
            db.session.delete(relation)
            db.session.delete(p)
            db.session.commit()
        elif request.form.get('edit') == 'confirm':
            session['productid'] = request.form['id']
            return  redirect(url_for('edit_product'))
        else:
            return redirect(url_for('add_product'))
    products = Products.query.all()
    p = []
    for i in products:
        p.append(i)
    return render_template('foodmart1/admin_products.html',product=p)
@app.route('/admin_categorys',methods=['GET','POST'])
def admin_category():
    if request.method == 'POST':
        if request.form.get('remove1') == "remove1":
            id = int(request.form['id'])
            ps = []
            relation = CategoryAndProduct.query.filter_by(categoryid=id).all()
            for i in relation:
                x = Products.query.filter_by(id=i.productid).first()
                ps.append(x)
            for i in ps:
                if i:
                    r = CategoryAndProduct.query.filter_by(productid=i.id).first()
                    db.session.delete(r)
                    db.session.commit()
            for i in ps:
                if i:
                    db.session.delete(i)
                    db.session.commit()
            c = Category.query.filter_by(id=id).first()
            db.session.delete(c)
            db.session.commit()
        elif request.form.get('edit') == 'confirm':
            # print(request.form['id'],'hihihitrhjoiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiisgtr\ng\ng\ng\ng\ng\ng\ng\ng\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            session['categoryid'] = request.form['id']
            return  redirect(url_for('edit_category'))
        else:
            return redirect(url_for('add_category'))
    category = Category.query.all()
    cat = []
    for i in category:
        cat.append(i)
    return render_template('foodmart1/admin_category.html',category=cat)
@app.route('/admin_customers',methods=['GET','POST'])
def admin_customer():
    if request.method == 'POST':
        if request.form.get('remove1') == "remove1":
            id = int(request.form['id'])
            p = Users.query.filter_by(id=id).first()
            relation = CategoryAndProduct.query.filter_by(productid=p.id).first()
            db.session.delete(relation)
            db.session.delete(p)
            db.session.commit()
    users = []
    u = Users.query.all()
    for i in u:
        users.append(i)
    return render_template('foodmart1/admin_customers.html',p=users)
@app.route('/add_category',methods=["GET","POST"])
def add_category():
    if request.method == "POST":
        name = request.form['name']
        desc = request.form['desc']
        cat = Category(name=name,description=desc)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('admin_category'))
    return render_template('foodmart1/add_category.html')
@app.route('/add_product',methods=["POST","GET"])
def add_product():
    if request.method == "POST":
        print('in proccess')
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        stock = request.form['stock']
        image = request.form['image']
        category = request.form['category']
        print('done variebles')

        cat = Products(name=name,about=desc,price=int(price),stock=int(stock),image=image)
        db.session.add(cat)
        db.session.commit()
        relation = CategoryAndProduct(productid=cat.id,categoryid=int(category))

        db.session.add(relation)
        db.session.commit()
        print('done')
        return redirect(url_for('admin_products'))
    return render_template('foodmart1/add_product.html')
@app.route('/edit_category',methods=["POST","GET"])
def edit_category():
    id = int(session['categoryid'])
    # print(id,type(id))
    if request.method == 'POST':
        print('in proccess')
        name = request.form['name']
        desc = request.form['desc']
        print(desc)
        id = int(session['categoryid'])
        print('cat debugg start')
        cat = Category.query.filter_by(id=int(id)).first()
        print('cat debugg end')
        if cat:
            print('yooooo')
            cat.name = name
            cat.description = desc
            db.session.commit()
        else:
            print("No product found with id", id)
        print('done')
        return redirect(url_for('admin_category'))
    i = Category.query.filter_by(id=id).first()
    return render_template('foodmart1/edit_category.html',info=i)
@app.route('/edit_product',methods=['POST','GET'])
def edit_product():
    id = int(session['productid'])
    print(id,type(id))
    if request.method == 'POST':
        print('in proccess')
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        stock = request.form['stock']
        image = request.form['image']
        category = request.form['category']
        print("Session contents:", dict(session))
        try:
            id = int(session['productid'])
            print("Got id from session:", id)
        except Exception as e:
            print("Problem with session['categoryid']:", e)
            return "No id found in session", 400

        print('cat debugg start')
        cat = Products.query.filter_by(id=int(id)).first()
        print('cat debugg end')
        if cat:
            print('yooooo')
            cat.name = name
            cat.about = desc
            cat.price = price
            cat.stock = stock
            cat.image = image
            cat.category = category
            db.session.commit()
        else:
            print("No product found with id", id)
        print('done')
        return redirect(url_for('admin_products'))
    i = Products.query.filter_by(id=id).first()
    return render_template('foodmart1/edit_product.html',info=i)

@app.route('/cart',methods=['GET','POST'])
def carts():
    # session['productamount'] = 0
    global user
    cartid = Carts.query.filter_by(user=int(session['id'])).first()
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











        if request.form.get("add1") == "add1":
            print(int(request.form['id']))
            product = Products.query.filter_by(id=int(request.form['id'])).first()
            if product:
                print(product)
            else:
                print('nuh uh')
            cart = Carts.query.filter_by(user=int(session['id'])).first()
            cart_product = CartProducts.query.filter_by(cartid=int(cart.id), productid=int(product.id)).first()
            if product.stock == 0:
                session['cart-message'] = 'sorry we have ran out!'
            else:
                print('adding')
                cart_product.amount += 1
                product.stock -= 1
                db.session.commit()
                session['productamount'] += 1
            print(session['productamount'])






    P_amount = str(session['productamount'])
    logged = session['logged']
    cartid = Carts.query.filter_by(user=int(session['id'])).first()
    cart_items = CartProducts.query.filter_by(cartid=int(cartid.id)).all()
    product_ids = [item.productid for item in cart_items]
    products = []
    for i in product_ids:
        x = Products.query.filter_by(id=int(i)).first()
        amounts = CartProducts.query.filter_by(productid=int(x.id)).first()
        amount = amounts.amount
        products.append([x,amount])
    return render_template('foodmart1/cartproducts.html',name=websitename,username=user,logged=logged,productamount=P_amount,products=products)


@app.route('/add_to_cart',methods=['GET','POST'])
def add_to_cart():
    if request.method == 'POST':
        if session['logged']:
            print(int(request.form['id']))
            product = Products.query.filter_by(id=int(request.form['id'])).first()
            if product:
                print(product)
            else:
                print('nuh uh')
            cart =     Carts.query.filter_by(user=int(session['id'])).first()
            cart_product = CartProducts.query.filter_by(cartid=int(cart.id),productid=int(product.id)).first()
            if cart_product:
                if product.stock == 0:
                    session['cart-message'] = 'sorry we have ran out!'
                else:
                    cart_product.amount += 1
                    product.stock -= 1
                    db.session.commit()
                    session['productamount'] += 1
            else:
                print()
                if product.stock == 0:
                    session['cart-message'] = 'sorry we have ran out!'
                else:
                    relation = CartProducts(cartid=int(cart.id),productid=int(product.id),amount=1)
                    product.stock -= 1
                    db.session.add(relation)
                    db.session.commit()
                    session['productamount'] += 1
            location = request.form['location']

            print(session['productamount'])
            return (redirect(url_for(str(location))))
        else:
            location = request.form['location']
            session['cart-message'] = 'Not logged in'
            return redirect(url_for(str(location)))


@app.route('/',methods=['GET','POST'])
def home():
    # if 'cart-message' in session:
    #     del session['cart-message']
    if 'logged' not in session:
        session['logged'] = False
    if 'productamount' not in session:
        if session['logged']:
            cart = Carts.query.filter_by(user=int(session['id'])).first()
            cartitems = CartProducts.query.filter_by(cartid=int(cart.id)).all()

            amount = 0
            for i in cartitems:
                print(i,i.amount)
                amount += int(i.amount)
            session['productamount'] = amount
        else:
            session['productamount'] = 0

    global user
    websitename = Connect.get_value('Name')
    user = ''
    if 'username' in session and session['logged']:
            user = session['username']
    amount = str(session['productamount'])
    logged = session['logged']
    print(logged,user)
    message = ''
    if 'cart-message' in session:
        message = session['cart-message']
    return render_template('foodmart1/main2.html',name=websitename,username=user,logged=logged,productamount=amount,message=message)
@app.route('/products')
def products():
    # if 'cart-message' in session:
    #     session['cart-message'] = ''
    if 'logged' not in session:
        session['logged'] = False
    # if 'productamount' not in session:
    #     session['productamount'] = 0

    global user
    websitename = Connect.get_value('Name')
    user = ''
    if 'username' in session and session['logged']:
            user = session['username']
    amount = str(session['productamount'])
    logged = session['logged']


    products = []
    P = Products.query.all()
    message = ''
    if 'cart-message' in session:
        message = session['cart-message']
    for i in P:
        if i.stock == 0:
            pass
        else:
            products.append(i)
    return render_template('foodmart1/products.html',name=websitename,username=user,logged=logged,productamount=amount,products=products,message=message)

@app.route('/loggout',methods=['GET','POST'])
def loggout():
    if request.method == 'POST':
        if request.form.get("action") == "logout":
            session['logged'] = False
            session['productamount'] = 0
            del session['username']
            del session['password']
            return redirect(url_for('home'))

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    session['cart-message'] = ''
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
    if 'logged' not in session:
        session['logged'] = False
    # if 'productamount' not in session:
    #     session['productamount'] = 0
    websitename = Connect.get_value('Name')
    user = ''
    if 'username' in session and session['logged']:
            user = session['username']
    amount = str(session['productamount'])
    logged = session['logged']
    # GET request - just render the contact form
    logged = session['logged']
    return render_template('foodmart1/contact-us.html',name=websitename,username=user,logged=logged,productamount=amount)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['cart-message'] = ''
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
                session['username'] = user.username
                session['password'] = user.password
                session['id'] = int(user.id)
                session['logged'] = True
                cart = Carts.query.filter_by(user=int(session['id'])).first()
                cartitems = CartProducts.query.filter_by(cartid=int(cart.id)).all()

                amount = 0
                for i in cartitems:
                    print(i, i.amount)
                    amount += int(i.amount)
                session['productamount'] = amount
                return redirect(url_for('home'))
            else:
                return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))
    return render_template('foodmart1/login.html')


@app.route('/admin', methods=['GET', 'POST'])
def Admin():
    session['cart-message'] = ''
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']


@app.route('/about_us',methods=['GET','POST'])
def about_us():
    session['cart-message'] = ''
    if 'logged' not in session:
        session['logged'] = False
    # if 'productamount' not in session:
    #     session['productamount'] = 0

    global user
    websitename = Connect.get_value('Name')
    user = ''
    if 'username' in session and session['logged']:
            user = session['username']
    amount = str(session['productamount'])
    logged = session['logged']
    return render_template('foodmart1/about_us.html',name=websitename,username=user,logged=logged,productamount=amount)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session['cart-message'] = ''
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

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        print('alright doing good')
        password = request.form['password']
        username = request.form['username']
        print('lol')
        adminrole = Roles.query.filter_by(name='Admin').first()
        user = Users.query.filter_by(username=username).first()
        print('finding account')
        if user:
            if check_password_hash(user.password,password):
                print('password is right')
                session['username'] = user.username
                session['password'] = user.password
                session['id'] = int(user.id)
                session['logged'] = True
                if int(user.roleid) == int(adminrole):
                    pass
                else:
                    return redirect(url_for('error'))

            else:
                return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))
        return redirect(url_for('dashboard'))
    return render_template('footmart1/admin_login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('foodmart1/dashboard.html')
@app.errorhandler(401)
def error401():
    return render_template('foodmart1/error.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    DF(app)
    app.run(debug=True)
