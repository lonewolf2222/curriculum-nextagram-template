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