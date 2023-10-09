import os
import requests
import json
from termcolor import colored
from datetime import timedelta
from datetime import datetime, timezone
import time
import sys
from simple_salesforce import Salesforce
import keyring

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def sendMail(to, title, brevoapikey, text):
  url = "https://api.brevo.com/v3/smtp/email"
  payload = json.dumps({
    "sender": {
      "name": "SFSC Robot",
      "email": "noreply@example.com"
    },
    "to": [
      {
        "email": to,
        "name": "Gabriele"
      }
    ],
    "subject": title,
    "htmlContent": text
  })
  headers = {
    'accept': 'application/json',
    'api-key': brevoapikey
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)


def main():
  print(colored("SFSC Prod Monitor v1.0", 'green'))
  f = open('config.json')
  data = json.load(f)
  user = data['user_to_monitor']
  email_to_notify = data['email_to_notify']
  brevoapikey = data['brevoapikey']
  interval = data['interval_in_seconds']

  startdate = (datetime.now(timezone.utc)-timedelta(minutes=+1)).strftime("%Y-%m-%dT%H:%M:%SZ")
  print('querying SF database from (UTC): '+startdate)
  query = "select id, Display, CreatedBy.Name, CreatedDate, Action from SetupAuditTrail where CreatedBy.username = '"+user+"' and createddate > "+startdate +" order by createddate desc limit 1000"

  while True:
    try: 
      print(colored("Checking ("+ str(datetime.now()) +") ...", 'green'))
      if (data['Production']):
        sf = Salesforce (
            username = data['SF_username'],
            password = keyring.get_password("SF_Monitor", "SF_Password"),
            security_token = keyring.get_password("SF_Monitor", "SF_Token"),
            instance_url = data['SF_instance_url']
        )
      else:
        sf = Salesforce (
          username = data['SF_username'],
          password = keyring.get_password("SF_Monitor", "SF_Password"),
          security_token = keyring.get_password("SF_Monitor", "SF_Token"),
          instance_url = data['SF_instance_url'],
          domain = 'test'
        )
      r = sf.query(query)
      if r['totalSize'] > 0:
        print(colored("Change Detected!!", 'red'))
        notify("Prod Change!!!", "Was it intentional?")
        sendMail(email_to_notify, "Prod Change!!!", brevoapikey, "<html><head></head><body><p>Hello,</p><p>We detect a prod change, please double check! </p><p>(email sent from Brevo)</p></body></html>")
      else:
        print(colored("No changes", 'green'))
      time.sleep(interval)
    except: 
      print(colored("Query Failed", 'red'))
      sendMail(email_to_notify, "Query Error", brevoapikey, "<html><head></head><body><p>Hello,</p><p>There was an issue in executing the query </p><p>(email sent from Brevo)</p></body></html>")
      time.sleep(interval*2)
  