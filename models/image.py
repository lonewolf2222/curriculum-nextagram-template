from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
AWS_S3_DOMAIN = "http://lonewolf2222-storage.s3.amazonaws.com/"

class Image(BaseModel):
    image_path = pw.CharField(null=True)
    desc = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def user_images_url(self):
        return AWS_S3_DOMAIN + self.image_path


    