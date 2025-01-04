# This code snippet is importing various modules and classes from different files within the project.
# Here's a breakdown of what each line is doing:
from flask_sqlalchemy import SQLAlchemy
from .auth import Auth
from .users import Users
from .device import Device
from .physiological.blood_oxygen import BloodOxygen
from .physiological.heart_rate import HeartRate

