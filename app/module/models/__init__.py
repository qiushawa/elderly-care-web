from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_device import *
from .device_data import *
from .device import *
from .auth import *