from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        
        if duplicate_username:
            self.errors.append('Username already exists!')
        if duplicate_email:
            self.errors.append('Email already exists!')

