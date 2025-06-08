from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
db = SQLAlchemy()
u = UniqueConstraint
