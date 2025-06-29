from flask import Flask,render_template,session,url_for,request,redirect
from flask_migrate import Migrate
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from config import  Config

app = Flask(__name__)
migrate = Migrate(app,db)
app.config.from_object(Config)
app.secret_key = "123"
db.init_app(app)
logged = False
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
    return render_template('main2.html')
# @app.route('/index')
# def index():
#     return 'hello'
# @app.route('/login')
# def login():
#     return 'hi'
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
    return render_template('login.html')
@app.route('/admin',methods=['GET','POST'])
def Admin():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
@app.route('/siging', methods=['GET','POST'])
def signin():
    global logged
    if 'username' in session:
        del session['username']
        del session['password']
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        logged = True
        return redirect(url_for('home'))
    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
