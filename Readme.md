
# Salesforce Production Change Monitoring

Imagine you are checking the configuration of different salesforce orgs, and eventually making some changes: it's so easy to make mistakes and apply those changes to the wrong org, since the only way to distinguish between them is to check the url!
Chrome Plugins like "Tab Modifier" and "Salesforce Production Warning" are great but, if you want to have an additional level of security, consider running this simple Python script in the background. It will promptly send email and notification center alerts if any alterations are detected in the org you intend to safeguard... most likely your production environment!

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
- SF_instance_url: URL of the target org
- SF_username: Salesforce username to connect to Salesforce
- Production: indicates whether the target org is production (true) or sandbox (false)


4) Set up your Salesforce Token and Password in the Keyring.
You can also use python:

```bash
  import keyring
  keyring.set_password("SF_Monitor", "SF_Password", <your_password>)
  keyring.set_password("SF_Monitor", "SF_Token", <your_token>)
```