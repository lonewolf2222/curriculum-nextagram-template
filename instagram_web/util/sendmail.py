import os
import requests
import yagmail

mailgun_domain = os.environ.get("MAILGUN_DOMAIN")
mydomain = os.environ.get("MY_DOMAIN")

sender_email=os.environ.get("sender_email")
sender_password=os.environ.get("sender_password")

# sender_email="homebox9091@gmail.com"
# sender_password="Xmen123456"
yag=yagmail.SMTP(user=sender_email, password=sender_password)

def send_email(sender, receiver_email, amount):
    subject="Congrats"
    contents=[f"You have received a donation of USD{amount} from {sender}"]
    yag.send(receiver_email, subject, contents)

def send_email_follow(sender, receiver_email):
    subject=f"Request to follow from {sender}"
    url=f'{mydomain}/follows/new'
    contents="""<html><head></head><body><p>Please click on the link below to review and approve </p> <br> <a href="{}">Click Here</a></body></html>""".format(url)
    yag.send(receiver_email, subject, contents)

def send_email_reset(receiver_email, reset_token):
    subject="Password Reset Request"
    url=f'{mydomain}/sessions/verify_token/{reset_token}'
    contents="""<html><head></head><body><p>Please click on the link below to set a new password </p> <br> <a href="{}">Click Here</a><br><p>You can ignore this email if you did not make this request </p></body></html>""".format(url)
    yag.send(receiver_email, subject, contents)

# def send_email(sender, receiver_email, amount):
#     return requests.post(
#         f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
#         auth=("api", os.environ.get("MAILGUN_API_KEY")),
#         data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
#               "to": [f"{receiver_email}"],
#               "subject": "Congrats!",
#               "text": f"You have received a donation of USD{amount} from {sender}!"})

# def send_email_follow(sender, receiver_email):
#     return requests.post(
#         f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
#         auth=("api", os.environ.get("MAILGUN_API_KEY")),
#         data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
#               "to": [f"{receiver_email}"],
#               "subject": f"Follow Request from {sender}!",
#               "text": f"Please click on the link to review and approve: {mydomain}/follows/new"})

# def send_email_reset(receiver_email, reset_token):
#     return requests.post(
#         f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
#         auth=("api", os.environ.get("MAILGUN_API_KEY")),
#         data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
#               "to": [f"{receiver_email}"],
#               "subject": "Password reset request received!",
#               "text": f"Please click on the link to reset your password: {mydomain}/sessions/verify_token/{reset_token}"})

