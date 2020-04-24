import os
import requests
# import yagmail
from threading import Thread

mailgun_domain = os.environ.get("MAILGUN_DOMAIN")
mydomain = os.environ.get("MY_DOMAIN")

# sender_email=os.environ.get("sender_email")
# sender_password=os.environ.get("sender_password")

# yag=yagmail.SMTP(user=sender_email, password=sender_password)

# def send_async_email(receiver_email, subject, contents):
#     yag.send(receiver_email, subject, contents)

def send_async_email(receiver_email, subject, contents):
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
              "to": [f"{receiver_email}"],
              "subject": f"{subject}",
              "html": f"{contents}"})

def send_email(sender, receiver_email, amount, image_url):
    subject="Congrats! You have received a donation"
    contents="""<html><head></head><body><p>Your photo below have received a donation of USD{} from {} </p> <br> <img src="{}" style="width:200px;height:200px"></body></html>""".format(amount, sender, image_url)
    Thread(target=send_async_email, args=(receiver_email, subject, contents)).start()

def send_email_follow(sender, receiver_email):
    subject=f"Request to follow from {sender}"
    url=f"{mydomain}/follows/new"
    contents="""<html><head></head><body><p>Please click on the link below to review and approve </p> <br> <a href="{}">Click To Approve</a></body></html>""".format(url)
    Thread(target=send_async_email, args=(receiver_email, subject, contents)).start()

def send_email_approved(sender, receiver_email):
    subject="Follow request approved"
    contents=f"Your request to follow {sender} has been approved."
    Thread(target=send_async_email, args=(receiver_email, subject, contents)).start()

def send_email_reset(receiver_email, reset_token):
    subject="Password Reset Request"
    url=f'{mydomain}/sessions/verify_token/{reset_token}'
    contents="""<html><head></head><body><p>Please click on the link below to set a new password </p> <br> <a href="{}">Click Here</a><br><p>You can ignore this email if you did not make this request </p></body></html>""".format(url)
    Thread(target=send_async_email, args=(receiver_email, subject, contents)).start()
    



