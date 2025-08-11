from . import db
role_permissions = db.Table('role_permissions',
                            db.Column('id',db.Integer,primary_key=True),
                            db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
                            )
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(40),unique=True)
    email = db.Column(db.String(60),unique=True)
    password = db.Column(db.String(198))
    roleid = db.Column(db.Integer,db.ForeignKey('roles.id'))

    role = db.relationship('Roles', back_populates='users')

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    description = db.Column(db.Text)
    permissions = db.relationship('Permision', secondary=role_permissions, back_populates='roles')
    users = db.relationship('Users', back_populates='role', lazy=True)
class Permision(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(50),unique=True,nullable=False)
    description = db.Column(db.Text)

    roles = db.relationship('Roles', secondary=role_permissions, back_populates='permissions')

# Role :
    # id:1 , name :guest
    # id:2 , name:customer ,

    # Permission
    # id:1 , role:1 , name:view product
    # id:2 , role:2 , name :view product,buy product