import os
import requests
mailgun_domain = os.environ.get("MAILGUN_DOMAIN")

def send_email(sender, receiver_email, amount):
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": f"Nextagram Admin <mailgun@{mailgun_domain}>",
              "to": [f"{receiver_email}"],
              "subject": "Congrats!",
              "text": f"You have received a donation of USD{amount} from {sender}!"})