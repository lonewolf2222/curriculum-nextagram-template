from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property, hybrid_method
AWS_S3_DOMAIN = "http://lonewolf2222-storage.s3.amazonaws.com/"

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    image_path = pw.CharField(unique=False, default='')
    private =pw.BooleanField(default=False)

    @hybrid_property
    def profile_image_url(self):
        return AWS_S3_DOMAIN + self.image_path

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        
        if duplicate_username:
            self.errors.append('Username already exists!')
        if duplicate_email:
            self.errors.append('Email already exists!')
    
    def is_private(self):
        return True if self.private else False

    def is_following(self, idol_id):
        from models.follow import IdolFan
        if IdolFan.get_or_none((IdolFan.idol_id == idol_id) & (IdolFan.fan_id == self.id)):
            return True
        else:
            return False


