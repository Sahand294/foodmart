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
from .address import *
from .brandcategory import *
from .brands import *
from .cart import *
from .category import *
from .discounts import *
from .manytomany import *
from .orders import *
from .paymentmethod import *
from .products import *
from .review import *
from .shippingmethod import *
from .sitesetting import *
from .users import *

