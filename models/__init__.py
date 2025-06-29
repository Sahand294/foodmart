from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import importlib
import os
db = SQLAlchemy()
u = UniqueConstraint

models_directory = os.path.dirname(__file__)

package_name = __name__

for filename in os.listdir(models_directory):

    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]

        importlib.import_module(f'{package_name}.{module_name}')

