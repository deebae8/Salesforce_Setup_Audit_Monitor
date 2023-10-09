
# Salesforce Production Change Monitoring

Working with different Salesforce instances increases the risk of unintentional changes to a Salesforce instance. To avoid surprises, consider running this simple Python script in the background. It will promptly send email and notification center alerts if any alterations are detected in the instance you intend to safeguard—most likely your production environment!

## Installation

1) Make sure python3 is installed

2) Install the requirements 

```bash
  pip3 install -f requirements.txt
```

3) Set up the following parameters in the config.json file: 
- user_to_monitor: username of the user to be monitored
- email_to_notify: email to send the notifications
- brevoapikey: the API KEY of Brevo service
- interval_in_seconds: frequency of checking (in seconds)
- SF_instance_url: Salesforce instance
- SF_username: Salesforce username to connect to Salesforce


4) Set up your Salesforce Token and Password in the Keyring.
You can also use python:

```bash
  import keyring
  keyring.set_password("SF_Monitor", "SF_Password", <your_password>)
  keyring.set_password("SF_Monitor", "SF_Token", <your_token>)
```