from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)

@app.route('/')
def home():
    print("111")
    return "Hello, World!"

@app.errorhandler(401)
def error_401(e):
    return render_template('error.html'), 401

if __name__ == '__main__':
    app.run(debug=True)
