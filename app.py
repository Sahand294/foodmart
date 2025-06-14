from flask import Flask,render_template
from flask_migrate import Migrate
from models import *
app = Flask(__name__)
migrate = Migrate(app,)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
