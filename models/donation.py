from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw

class Donation(BaseModel):
    amount = pw.DecimalField(unique=False, null=False)
    user = pw.ForeignKeyField(User, backref="donations")
    image = pw.ForeignKeyField(Image, backref="donations")