import boto3, botocore
from config import Config
import re

def password_checker(password):
    errors=[]
    if len(password) < 6:
        errors.append("Password must be at least 6 characters")
    if re.search('[0-9]', password) is None:
        errors.append("Password must have at least one number")
    if re.search('[a-z]', password) is None:
        errors.append("Password must have at least one lower case letter")
    if re.search('[A-Z]', password) is None:
        errors.append("Password must have at least one capital letter")
    if re.search('[^A-Za-z\s0-9]', password) is None:
        errors.append("Password must have at least one special character")
    return errors

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)

def upload_file_to_s3(file, acl="public-read"):

    try:
        s3.upload_fileobj(
            file,
            Config.S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    
    return "{}{}".format(Config.S3_LOCATION, file.filename)