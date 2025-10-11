from flask import Flask, render_template, session, url_for, request, redirect, flash, Blueprint, jsonify, \
    render_template_string
from flask_migrate import Migrate
from config import Config
from sending_emails import Send
import re
from models.orders import Orders,Order_items
import dns.resolver
from add_account import AddAccounts
from default_values import DF, Add_Values
from models import db
from models.sitesetting import SiteSetting
from default_connection import Connect
from default_permissions import DF_P, Add_Connection
from models import Users, Roles
from models.cart import Carts, CartProducts
import stripe
from models.orders import Orders
from models.manytomany import CategoryAndProduct
from models.category import Category
from models.products import Products
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import secrets
import string
from decimal import Decimal, ROUND_HALF_UP
load_dotenv()

# Function to generate a secure random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


stripe.api_key = "sk_test_51S9OlcDbgzKCvypomEvrVhNMuKwDGOrLguD75RpC64dQJXeyTP2MYksXBKlsa68Q8OENB9ndns1GsEBs982nyn4V0058oqhGNg"



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
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ['true', 'True', '1']:
            return True
    return False


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = '123'
db.init_app(app)
migrate = Migrate(app, db)
app.jinja_env.globals.update(zip=zip)
app.jinja_env.filters['zip'] = zip

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

        Add_Values(logo, name, smtp_user, receiver, template, 'True',
                   smtp_port, smtp_server, smtp_pass, username, password, firstname, lastname, email)
        session['websitename'] = Connect.get_value('Name')
        return redirect(url_for('home'))

    return render_template('foodmart1/install.html')

if True:
    # @app.route('/admin_products', methods=["POST", "GET"])
    # def admin_products():
    #     if request.method == "POST":
    #         if request.form.get('remove1') == "remove1":
    #             id = int(request.form['id'])
    #             p = Products.query.filter_by(id=id).first()
    #             relation = CategoryAndProduct.query.filter_by(productid=p.id).first()
    #             db.session.delete(relation)
    #             db.session.delete(p)
    #             db.session.commit()
    #         elif request.form.get('edit') == 'confirm':
    #             session['productid'] = request.form['id']
    #             return redirect(url_for('edit_product'))
    #         else:
    #             return redirect(url_for('add_product'))
    #     products = Products.query.all()
    #     product_categories = {}
    #     p = []
    #     for i in  products:
    #         rel = CategoryAndProduct.query.filter_by(productid=i.id).all()
    #         name = []
    #         for x in rel:
    #             cat = Category.query.filter_by(id=x.categoryid).first()
    #             name.append(str(cat.name))
    #         p.append(i,name)
    #     # for i in products:
    #     #     cate = CategoryAndProduct.query.filter_by(productid=int(i.id)).all()
    #     #     for u in cate:
    #     #         c.append(u)
    #     category = Category.query.all()
    #     return render_template('foodmart1/admin_products.html', product=products,cat=category)
    @app.route('/admin_products', methods=["POST", "GET"])
    def admin_products():
        if session['role'] == 'Admin' or session['role'] == 'Owner':

            if request.method == "POST":
                if request.form.get('remove1') == "remove1":
                    id = int(request.form['id'])
                    p = Products.query.filter_by(id=id).first()
                    stripe.Product.modify(p.product_stripe_id, active=False)
                    stripe.Price.modify(p.product_price_stripe_id, active=False)
                    relations = CategoryAndProduct.query.filter_by(productid=p.id).all()
                    relis = CartProducts.query.filter_by(productid=p.id).all()
                    print(relis,p.id)
                    print(relations)
                    for rel,l in zip(relations,relis):
                        db.session.delete(rel)
                        db.session.commit()
                        db.session.delete(l)
                        db.session.commit()
                    db.session.commit()
                    db.session.delete(p)
                    db.session.commit()
                elif request.form.get('edit') == 'confirm':
                    session['productid'] = request.form['id']
                    return redirect(url_for('edit_product'))
                else:
                    return redirect(url_for('add_product'))

            products = Products.query.all()

            product_categories = {}
            # for p in products:
            #     print('hello')
            #     relations = CategoryAndProduct.query.filter_by(productid=p.id).all()
            #     for r in relations:
            #         print('relation:::::::::',r.categoryid,'product:',r.productid)
            #     product_categories[p.id] = [db.session.get(Category, rel.categoryid) for rel in relations]
            category = Category.query.all()
            return render_template('foodmart1/admin_products.html', product=products,product_categories=product_categories,cat=category)
        else:
            return redirect(url_for('home'))

    @app.route('/admin_categorys', methods=['GET', 'POST'])
    def admin_category():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
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
                    return redirect(url_for('edit_category'))
                else:
                    return redirect(url_for('add_category'))
            category = Category.query.all()
            cat = []
            for i in category:
                cat.append(i)
            return render_template('foodmart1/admin_category.html', category=cat)
        else:
            return redirect(url_for('home'))

    @app.route('/admin_customers', methods=['GET', 'POST'])
    def admin_customer():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
            if request.method == 'POST':
                if request.form.get('remove1') == "remove1":
                    id = int(request.form['id'])
                    p = Users.query.filter_by(id=id).first()
                    cart = Carts.query.filter_by(user=int(p.id)).first()
                    relation = CartProducts.query.filter_by(cartid=cart.id).all()
                    try:
                        for i in relation:
                            print(i.cartid)
                            productid = int(i.productid)
                            product = Products.query.filter_by(id=int(productid)).first()
                            quantity = int(i.amount)
                            product.stock += quantity
                            cartitem = CartProducts.query.filter_by(productid=productid).first()
                            db.session.delete(cartitem)
                            db.session.commit()
                        db.session.delete(cart)
                        db.session.commit()
                        db.session.delete(p)
                        db.session.commit()
                    except:
                        print('not worked')
                elif request.form.get('edit') == 'confirm':
                    print('going to it')
                    session['userid'] = request.form.get('id')
                    print(session['userid'])
                    return redirect(url_for('edit_customer'))
            users = []
            u = Users.query.all()
            for i in u:
                role = Roles.query.filter_by(id=int(i.roleid)).first()
                k = 0
                s = session['role']
                if role.name == 'Customer' and s == 'Admin':
                    n = Carts.query.filter_by(user=int(i.id)).first()
                    rel = CartProducts.query.filter_by(cartid=int(n.id)).all()
                    for u in rel:

                        k += int(u.amount)
                    print('ammount', k)
                    users.append([i,k])
                else:
                    n = Carts.query.filter_by(user=int(i.id)).first()
                    rel = CartProducts.query.filter_by(cartid=int(n.id)).all()
                    for u in rel:

                        k += int(u.amount)
                    print('ammount', k)
                    users.append([i,k])
            return render_template('foodmart1/admin_customers.html', p=users)
        else:
            return redirect(url_for('home'))
    @app.route('/view_orders')
    def view_order():
        order_id = int(session['order_id'])
        del session['order_id']
        # users_in_usa = (User.query
        #                 .join(Address_User).join(City).join(ProvinceOrTerritories).join(Country).filter(Country.name == 'United States').all())

        # Updated by JavadSarlak------------
        order_with_details = Orders.query\
            .join(Order_items, Orders.items)\
            .join(Products, Order_items.product_id == Products.id)\
            .filter(Orders.id == order_id)\
            .add_entity(Order_items)\
            .add_entity(Products)\
            .all()
        print(order_with_details)
        return render_template('foodmart1/view_order.html',rel=order_with_details)
    @app.route('/edit_customer', methods=['POST', 'GET'])
    def edit_customer():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
            print(session['userid'])
            u = Users.query.filter_by(id=int(session['userid'])).first()
            # del session['userid']
            if request.method == 'POST':
                print('doing it')
                firstname = request.form.get('firstname')
                lastname = request.form.get('lastname')
                username = request.form.get('username')
                email = request.form.get('email')
                print('saved stuff')
                if not is_real_email(email):
                    mistakes.append("Email is Wrong")
                else:
                    print('doing it')
                    password = generate_password()
                    subject = f"Hello {firstname}"
                    body =  f"""
                                    Hello {firstname} {lastname},
                                    
                                    Your account has been successfully created/updated by our administrator.
                                    
                                    Here are your login details:
                                    - Email: {email}
                                    - Username: {username}
                                    - Password: {password}
                                    - Firstname: {firstname}
                                    - Lastname: {lastname}
                                    
                                    For security, please log in and change your password as soon as possible:
                                    https://yourwebsite.com/login
                                    
                                    If you have any questions or need support, please contact us at support@yourwebsite.com.
                                    
                                    Best regards,
                                    The YourWebsite Team
                                    """

                    Send.send_mail(subject, email, body, email, False)
                    u.firstname = firstname
                    u.lastname = lastname
                    u.username = username
                    u.email = email
                    db.session.commit()
                    return redirect(url_for('dashboard'))
            return render_template('foodmart1/edit_customers.html')
        else:
            return redirect(url_for('home'))

    @app.route('/add_customers', methods=['POST', 'GET'])
    def add_customer():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
            global mistakes
            if request.method == 'POST':
                session['cart-message'] = ''
                print('making account')
                mistakes = []
                if request.method == 'POST':
                    firstname = request.form.get('firstname', '').strip()
                    lastname = request.form.get('lastname', '').strip()
                    email = request.form.get('email', '').strip()
                    username = request.form.get('username', '').strip()

                    if not is_real_email(email):
                        mistakes.append("Email is Wrong")
                    else:
                        password = generate_password()
                        subject = f"Hello {firstname}"
                        body = f"""
                                        Hello {firstname} {lastname},
        
                                        Your account has been successfully created/updated by our administrator.
        
                                        Here are your login details:
                                        - Email: {email}
                                        - Username: {username}
                                        - Password: {password}
                                        - Firstname: {firstname}
                                        - Lastname: {lastname}
        
                                        For security, please log in and change your password as soon as possible:
                                        https://yourwebsite.com/login
        
                                        If you have any questions or need support, please contact us at support@yourwebsite.com.
        
                                        Best regards,
                                        The YourWebsite Team
                                        """
                        Send.send_mail(subject, email, body, email, False)
                        AddAccounts.add(email, firstname, lastname, username, password)
                        return redirect(url_for('dashboard'))
            return render_template('foodmart1/add_customer_from_dashboard.html')
        else:
            return redirect(url_for('home'))

    @app.route('/add_category', methods=["GET", "POST"])
    def add_category():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
            if request.method == "POST":
                name = request.form['name']
                desc = request.form['desc']
                cat = Category(name=name, description=desc)
                db.session.add(cat)
                db.session.commit()
                return redirect(url_for('admin_category'))
            return render_template('foodmart1/add_category.html')
        else:
            return redirect(url_for('home'))

    @app.route('/add_product', methods=["POST", "GET"])
    def add_product():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
            if request.method == "POST":
                print('in proccess')
                name = request.form['name']
                desc = request.form['desc']
                price = request.form['price']
                stock = request.form['stock']
                image = request.form['image']
                category = request.form.getlist('category')
                print('done variebles')
                amt = Decimal(str(price))
                # Round to 2 decimal places to be safe (cents precision)
                amt = amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                # Multiply by 100 to get cents
                cents = int(amt * 100)
                s_product = stripe.Product.create(
                    name=name,
                    description=desc
                )

                # Create price for that product
                s_price = stripe.Price.create(
                    product=s_product.id,
                    unit_amount=cents,  # in cents, e.g. $20.00
                    currency="usd",
                )
                cat = Products(name=name, about=desc, price=int(price), stock=int(stock), image=image,product_stripe_id=s_product.id,product_price_stripe_id=s_price.id)
                db.session.add(cat)
                db.session.commit()
                for i in category:
                    relation = CategoryAndProduct(productid=cat.id, categoryid=int(i))
                    db.session.add(relation)
                    db.session.commit()
                print('done')


                return redirect(url_for('admin_products'))
            cats = Category.query.all()
            return render_template('foodmart1/add_product.html',cats=cats)
        else:
            return redirect(url_for('home'))

    @app.route('/edit_category', methods=["POST", "GET"])
    def edit_category():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
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
            return render_template('foodmart1/edit_category.html', info=i)
        else:
            return redirect(url_for('home'))

    @app.route('/edit_product', methods=['POST', 'GET'])
    def edit_product():
        if session['role'] == 'Admin' or session['role'] == 'Owner':
            id = int(session['productid'])
            print(id, type(id))
            if request.method == 'POST':
                print('in proccess')
                name = request.form['name']
                desc = request.form['desc']
                price = request.form['price']
                stock = request.form['stock']
                image = request.form['image']
                category = request.form.getlist('category')
                print("Session contents:", dict(session))
                try:
                    id = int(session['productid'])
                    print("Got id from session:", id)
                except Exception as e:
                    print("Problem with session['categoryid']:", e)
                    return "No id found in session", 400
                print('cat debugg start')
                cat = Products.query.filter_by(id=int(id)).first()


                amt = Decimal(str(price))
                amt = amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                cents = int(amt * 100)
                # update product name or description
                product = stripe.Product.modify(
                    cat.product_stripe_id,  # your existing product's id
                    name=name,
                    description=desc
                )

                # create a new price under the same product
                new_price = stripe.Price.create(
                    product=product.id,
                    unit_amount=cents,
                    currency="usd"
                )

                # deactivate the old price so only the new one is used
                stripe.Price.modify(
                    cat.product_price_stripe_id,  # your old price object's id
                    active=False
                )
                print('cat debugg end')
                if cat:
                    print('yooooo')
                    cat.name = name
                    cat.about = desc
                    cat.price = price
                    cat.stock = stock
                    cat.image = image
                    cat.product_price_stripe_id = new_price.id
                    for i in category:
                        print(type(i),category)
                        rel = CategoryAndProduct.query.filter_by(productid=cat.id).first()
                        db.session.delete(rel)
                        db.session.commit()
                        relation = CategoryAndProduct(productid=cat.id, categoryid=int(i))
                        db.session.add(relation)
                        db.session.commit()
                    db.session.commit()
                else:
                    print("No product found with id", id)
                print('done')
                return redirect(url_for('admin_products'))
            i = Products.query.filter_by(id=id).first()
            cats = Category.query.all()
            return render_template('foodmart1/edit_product.html', info=i,cats=cats)
        else:
            return redirect(url_for('home'))

@app.route('/cart', methods=['GET', 'POST'])
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
            print(request.form.get("id"))
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
            print(productid)
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
    amount_of_P = 0
    totall_price = 0
    products = []
    for i in product_ids:
        x = Products.query.filter_by(id=int(i)).first()
        amounts = CartProducts.query.filter_by(productid=int(x.id)).first()
        amount = amounts.amount
        products.append([x, amount])
        amount_of_P += 1
        totall_price += int(x.price * amount)
    # for i in products:
    #     print(i[0].id)
    # print(products)
    return render_template('foodmart1/cartproducts.html', name=websitename, username=user, logged=logged,
                           productamount=P_amount,
                           products=products, totall_price=totall_price, amount_of_P=amount_of_P)


@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        if session['logged']:
            print(int(request.form['id']))
            product = Products.query.filter_by(id=int(request.form['id'])).first()
            if product:
                print(product)
            else:
                print('nuh uh')
            cart = Carts.query.filter_by(user=int(session['id'])).first()
            cart_product = CartProducts.query.filter_by(cartid=int(cart.id), productid=int(product.id)).first()
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
                    relation = CartProducts(cartid=int(cart.id), productid=int(product.id), amount=1)
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

@app.route('/admin_orders',methods=['POST','GET'])
def orders():
    if request.method == 'POST':
        session['order_id'] = request.form.get('id')
        return redirect(url_for('view_order'))
    o = Orders.query.all()
    p = Products.query.all()
    Os = []
    products = []
    for i in o:
        Os.append(i)
        print(i)
    return render_template('foodmart1/orders.html',o=Os)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        cart = Carts.query.filter_by(user=int(session['id'])).first()
        rel = CartProducts.query.filter_by(cartid=cart.id).all()
        products = []
        print(cart.id)
        print(rel)
        for i in rel:
            print(i)
            p = Products.query.filter_by(id=int(i.productid)).first()
            products.append(p)
            print(p)
        print(products)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id.product_price_stripe_id,
                    'quantity': int(qty.amount)
                }
                for price_id, qty in zip(products, rel)
            ]
            ,
            mode='payment',
            success_url="http://127.0.0.1:5000" + '/success',
            cancel_url="http://127.0.0.1:5000" + '/fail',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
@app.route('/success')
def success():
    return render_template('foodmart1/success.html')
@app.route('/settings',methods=['GET','POST'])
def usersettings():
    user = Users.query.filter_by(id=int(session['id'])).first()
    orders = Orders.query.filter_by(users_email=user.email).order_by(Orders.id.desc()).limit(4).all()
    if request.method == "POST":
        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('emails', '').strip()
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()

        update_fields = {}
        if firstname:
            update_fields['firstname'] = firstname
        if lastname:
            update_fields['lastname'] = lastname
        if username:
            update_fields['username'] = username
        if email:
            update_fields['email'] = email
        if new_password:
            if check_password_hash(user.password, old_password):
                update_fields['password'] = AddAccounts.encrypting_password(new_password)
            else:
                flash('Current password is incorrect', 'error')
                return render_template('foodmart1/userprofile.html', u=user, orders=orders)
        if update_fields:
            for field, value in update_fields.items():
                setattr(user, field, value)
            db.session.commit()
    return render_template('foodmart1/usersetting.html',orders=orders,u=user)
@app.route('/profile',methods=['Get','POST'])
def profile():
    user = Users.query.filter_by(id=int(session['id'])).first()
    orders = Orders.query.filter_by(users_email=user.email).order_by(Orders.id.desc()).limit(4).all()

    return render_template('foodmart1/userprofile.html', u=user, orders=orders)
@app.route('/orders')
def userorders():
    user = Users.query.filter_by(id=int(session['id'])).first()
    orders = Orders.query.filter_by(users_email=user.email).all()
    return render_template('foodmart1/userorder.html',orders=orders,u=user)
@app.route('/fail')
def cancel():
    return render_template('foodmart1/cancel.html')
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'role' not in session:
        session['role']= 'guest'
    if 'logged' not in session:
        session['logged'] = False
    if 'productamount' not in session:
        if session['logged']:
            cart = Carts.query.filter_by(user=int(session['id'])).first()
            cartitems = CartProducts.query.filter_by(cartid=int(cart.id)).all()

            amount = 0
            for i in cartitems:
                # print(i, i.amount)
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
    # print(logged, user)
    message = ''
    if 'cart-message' in session:
        message = session['cart-message']
    print('hi',os.getenv("STRIPE_SECRET_KEY"))
    return render_template('foodmart1/main2.html', name=websitename, username=user, logged=logged, productamount=amount,
                           message=message)


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

    return render_template('foodmart1/products.html', name=websitename, username=user, logged=logged,
                           productamount=amount, products=products, message=message)


@app.route('/loggout', methods=['GET', 'POST'])
def loggout():
    if request.method == 'POST':
        if request.form.get("action") == "logout":
            session['logged'] = False
            session['productamount'] = 0
            session['role'] = 'guest'
            del session['username']
            del session['password']
            return redirect(url_for('home'))


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    session['cart-message'] = ''
    global name, user
    if 'websitename' in session:
        name = session['websitename']
    if 'username' in session:
        user = session['username']
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
            Send.send_mail(subject, email, body, email, contactus=True)
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
    return render_template('foodmart1/contact-us.html', name=websitename, username=user, logged=logged,
                           productamount=amount)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['cart-message'] = ''
    if request.method == 'POST':
        print('alright doing good')
        password = request.form['password']
        username = request.form['username']
        print('lol')
        user = Users.query.filter_by(username=username).first()
        print('finding account')
        if user:
            if check_password_hash(user.password, password):
                print('password is right')
                session['username'] = user.username
                session['password'] = user.password
                session['id'] = int(user.id)
                session['logged'] = True
                cart = Carts.query.filter_by(user=int(session['id'])).first()
                cartitems = CartProducts.query.filter_by(cartid=int(cart.id)).all()
                r = Roles.query.filter_by(id=user.roleid).first()
                session['role'] = r.name
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


@app.route('/about_us', methods=['GET', 'POST'])
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
    return render_template('foodmart1/about_us.html', name=websitename, username=user, logged=logged,
                           productamount=amount)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session['cart-message'] = ''
    print('making account')
    mistakes = ''
    if request.method == 'POST':
        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not is_real_email(email):
            mistakes = "Email is Wrong"
        else:
            # if not errors:
            #     print('must signup')
            AddAccounts.add(email, firstname, lastname, username, password)
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('foodmart1/signin.html', errors=mistakes)


# @app.route('/admin_login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         print('alright doing good')
#         password = request.form['password']
#         username = request.form['username']
#         print('lol')
#         adminrole = Roles.query.filter_by(name='Admin').first()
#         user = Users.query.filter_by(username=username).first()
#         print('finding account')
#         if user:
#             if check_password_hash(user.password, password):
#                 print('password is right')
#                 session['username'] = user.username
#                 session['password'] = user.password
#                 session['id'] = int(user.id)
#                 session['logged'] = True
#                 if int(user.roleid) == int(adminrole):
#                     pass
#                 else:
#                     return redirect(url_for('error'))
#
#             else:
#                 return redirect(url_for('error'))
#         else:
#             return redirect(url_for('error'))
#         return redirect(url_for('dashboard'))
#     return render_template('footmart1/admin_login.html')


@app.route('/dashboard')
def dashboard():
    if session['role'] == 'Admin' or session['role'] == 'Owner':
        return render_template('foodmart1/dashboard.html')
    else:
        return redirect(url_for('home'))

@app.route('/error401')
def error():
    return render_template('foodmart1/error.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    DF(app)
    app.run(debug=True)
