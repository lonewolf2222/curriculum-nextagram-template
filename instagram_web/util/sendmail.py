import os
import requests
from flask import url_for
mailgun_domain = os.environ.get("MAILGUN_DOMAIN")
mydomain = os.environ.get("MY_DOMAIN")

def send_email(sender, receiver_email, amount):
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
              "to": [f"{receiver_email}"],
              "subject": "Congrats!",
              "text": f"You have received a donation of USD{amount} from {sender}!"})

def send_email_follow(sender, receiver_email):
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
              "to": [f"{receiver_email}"],
              "subject": f"Follow Request from {sender}!",
              "text": f"Please click on the link to review and approve: {mydomain}/follows/new"})

# def send_email_follow(sender, receiver_email):
#     return requests.post(
#         f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
#         auth=("api", os.environ.get("MAILGUN_API_KEY")),
#         data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
#               "to": [f"{receiver_email}"],
#               "subject": f"Follow Request from {sender}!",
#               "html": "<p> please click on button to approve </p>
#                         <form action="{{url_for('follows.edit', fan_username =request.fan.username)}}" method="POST">
#                         <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
#                         <button type="submit" class="btn btn-info">Approve</button>
#                         </form>")
