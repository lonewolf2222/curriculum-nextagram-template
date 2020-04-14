from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import os

AWS_S3_DOMAIN = os.environ.get("AWS_S3_DOMAIN")

class Image(BaseModel):
    image_path = pw.CharField(null=True)
    desc = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def user_images_url(self):
        return AWS_S3_DOMAIN + self.image_path
    
    @hybrid_property
    def image_owner(self):
        return self.user.username


    