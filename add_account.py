from werkzeug.security import generate_password_hash,check_password_hash
from models.users import   Users,Roles
from models import db
from models.cart import Carts
class AddAccounts:
    @staticmethod
    def encrypting_password(password):
        """
        Hashes the given password using PBKDF2 + SHA256.
        :param password: Plaintext password string
        :return: Hashed password string
        """
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    @staticmethod
    def add(email,firstname,lastname,username,password,role='Customer'):
        roleid = Roles.query.filter_by(name=role).first()
        print('created')
        new_password = AddAccounts.encrypting_password(password)
        user = Users(firstname=firstname,lastname=lastname,username=username,email=email,password=new_password,roleid=int(roleid.id))
        db.session.add(user)
        db.session.commit()
        userid = Users.query.filter_by(email=email).first()
        cart = Carts(user=int(userid.id))
        db.session.add(cart)
        db.session.commit()
        print('done')