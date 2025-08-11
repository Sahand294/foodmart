from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import importlib
import os
db = SQLAlchemy()
u = UniqueConstraint

models_directory = os.path.dirname(__file__)

package_name = __name__

from .users import *
from .cart import *
from .sitesetting import *

