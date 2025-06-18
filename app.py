from flask import Flask,render_template,session,url_for,request,redirect
from flask_migrate import Migrate
from models import *
app = Flask(__name__)
migrate = Migrate(app,)
app.secret_key = "123"
logged = False
@app.route('/')
def home():  # put application's code here
    global logged
    user = ''
    if 'username' in session:
        if logged:
            print('yes')
            user = session['username']
    elif 'username' in session:
        del session['username']
        del session['password']
    return render_template('foodmart1/home.html',user=user)
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
    app.run()
