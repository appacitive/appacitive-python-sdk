__author__ = 'sathley'

from pyappacitive import AppacitiveEmail

def send_email_test_with_config():
    response = AppacitiveEmail.send_raw_email(['sathley@appacitive.com'], 'hello from py sdk', 'Wazza!', smtp={
        "username": "sathley@appacitive.com",
		"password": "########",
		"host": "smtp.gmail.com",
		"port": 465,
		"enablessl": True
    }, from_email='sathley@appacitive.com')

    assert response.status.code == '200'


def send_email_test_without_config():
    response = AppacitiveEmail.send_raw_email(['sathley@appacitive.com'], 'hello from py sdk', 'Wazza!', from_email='sathley@appacitive.com')

    assert response.status.code == '200'
