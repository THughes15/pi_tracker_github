# pi_tracker_github

Project to track the inventory status of Raspberry Pi Models from thepihut.com,
the code uses beutifulsoup4 and requests module to check the status of various Pi models,
and smtplib to send an email each time the status changes.

Before runnning, Config.py needs to be updated to include desired Sender and Reciever Email addresses,
along with sender email exchange info, and password.
(For gmail, the password required is an app password, not the password used to sign into the account, may be the same for other exchanges)
