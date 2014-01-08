__author__ = 'sathley'

from pyappacitive import AppacitiveEmail
import nose


def send_email_with_config_test():
    to = ['sathley@appacitive.com']
    cc = []
    bcc = []
    smtp = {
        "username": "sathley@appacitive.com",
	    "password": "########",
	    "host": "smtp.gmail.com",
	    "port": 465,
	    "enablessl": True
    }
    AppacitiveEmail.send_raw_email(to=to, cc=cc, bcc=bcc, body='hello from py sdk', subject='Wazza !', smtp=smtp, from_email_address='sathley@appacitive.com', reply_to_email_address='support@appacitive.com', is_body_html=False)


def send_email_without_config_test():
    to = ['sathley@appacitive.com']
    cc = []
    bcc = []
    AppacitiveEmail.send_raw_email(to=to, cc=cc, bcc=bcc, body='hello from py sdk', subject='Wazza !', from_email_address='sathley@appacitive.com', reply_to_email_address='support@appacitive.com')


def send_templated_email_test():
    template_fillers = {
        'username': 'john.doe',
        'firstname': 'John',
        'lastname': 'Doe'
    }
    to = ['sathley@appacitive.com']
    cc = []
    bcc = []
    smtp = {
        "username": "sathley@appacitive.com",
	    "password": "########",
	    "host": "smtp.gmail.com",
	    "port": 465,
	    "enablessl": True
    }
    AppacitiveEmail.send_templated_email(to=to, cc=cc, bcc=bcc, smtp=smtp, subject='Hello from py sdk', template_name='sample', template_fillers=template_fillers, is_body_html=True, from_email_address='sathley@appacitive.com', reply_to_email_address='support@appacitive.com')
