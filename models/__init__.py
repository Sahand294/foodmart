from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import importlib
import os
db = SQLAlchemy()
u = UniqueConstraint
models_direction = os.path.dirname(__file__)
for i in os.listdir(models_direction):
    if i.endswith('.py') and not i.startswith('__'):
        module_name = i[:-3]
        importlib.import_module(f'{module_name}')