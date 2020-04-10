import os
import requests

def send_email(sender, receiver_email, amount):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox0f93fa3b72844f8a8e032b010cba38ea.mailgun.org/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": "Nextagram Admin <mailgun@sandbox0f93fa3b72844f8a8e032b010cba38ea.mailgun.org>",
              "to": [f"{receiver_email}"],
              "subject": "Congrats!",
              "text": f"You have received a donation of USD{amount} from {sender}!"})