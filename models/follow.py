from models.base_model import BaseModel
from models.user import User
import peewee as pw
from flask_login import UserMixin

class IdolFan(BaseModel):
    idol = pw.ForeignKeyField(User, backref='fans')
    fan = pw.ForeignKeyField(User, backref='idols')
    approved = pw.BooleanField(default=False)
