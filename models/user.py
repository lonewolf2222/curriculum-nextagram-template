from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property, hybrid_method
import os


AWS_S3_DOMAIN = os.environ.get("AWS_S3_DOMAIN")

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
        if self.private:
            return True
        else:
            return False
    
    @hybrid_property
    def donation_given(self):
        donation_given = 0
        for d in self.donations:
            donation_given = donation_given + d.amount
        donation_given = round(donation_given, 2)
        return donation_given
    
    @hybrid_property
    def donation_received(self):
        from models.donation import Donation
        from models.image import Image
        donation_r = Donation.select().join(Image, on=(Donation.image_id == Image.id)).where(Image.user_id == self.id)
        donation_received = 0
        for d in donation_r:
            donation_received = donation_received + d.amount
        donation_received = round(donation_received, 2)
        return donation_received

    def is_following(self, idol_id):
        from models.follow import IdolFan
        if IdolFan.get_or_none((IdolFan.idol_id == idol_id) & (IdolFan.fan_id == self.id)):
            return True
        else:
            return False
    
    def is_approved(self, idol_id):
        from models.follow import IdolFan
        if IdolFan.get_or_none((IdolFan.idol_id == idol_id) & (IdolFan.fan_id == self.id) & (IdolFan.approved == True)):
            return True
        else:
            return False

    @hybrid_property
    def fans(self):
        from models.follow import IdolFan
        return User.select().join(IdolFan, on=(User.id == IdolFan.fan_id)).where(IdolFan.idol_id == self.id).where(IdolFan.approved == True)
    
    @hybrid_property
    def idols(self):
        from models.follow import IdolFan
        return User.select().join(IdolFan, on=(User.id == IdolFan.idol_id)).where(IdolFan.fan_id == self.id).where(IdolFan.approved == True)
    
    @hybrid_property
    def image_feed(self):
        from models.follow import IdolFan
        from models.image import Image
        return Image.select().join(IdolFan, on=(IdolFan.idol_id == Image.user_id)).where(IdolFan.fan_id == self.id).where(IdolFan.approved == True).order_by(Image.created_at.desc())



