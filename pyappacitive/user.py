__author__ = 'sathley'

from object import AppacitiveObject
from entity import object_system_properties
from error import ValidationError, UserAuthError
from utilities import http, urlfactory, appcontext
import json


def user_auth_required(func):

        def inner(*args, **kwargs):

            if appcontext.ApplicationContext.get_user_token() is None:
                raise UserAuthError('No logged in user found. Call authenticate first.')
            return func(*args, **kwargs)

        return inner


class AppacitiveUser(AppacitiveObject):

    def __init__(self, user=None):
        super(AppacitiveUser, self).__init__(user)
        self.type = 'user'

    user_auth_header_key = 'Appacitive-User-Auth'

    def __set_self(self, user):
        super(AppacitiveUser, self)._set_self(user)

    @property
    def username(self):
        return self.get_property('username')

    @username.setter
    def username(self, value):
        self.set_property('username', value)

    @property
    def location(self):
        return self.get_property('location')

    @location.setter
    def location(self, value):
        self.set_property('location', value)

    @property
    def email(self):
        return self.get_property('email')

    @email.setter
    def email(self, value):
        self.set_property('email', value)

    @property
    def firstname(self):
        return self.get_property('firstname')

    @firstname.setter
    def firstname(self, value):
        self.set_property('firstname', value)

    @property
    def lastname(self):
        return self.get_property('lastname')

    @lastname.setter
    def lastname(self, value):
        self.set_property('lastname', value)

    @property
    def birthdate(self):
        return self.get_property('birthdate')

    @birthdate.setter
    def birthdate(self, value):
        self.set_property('birthdate', value)

    @property
    def isemailverified(self):
        return self.get_property('isemailverified')

    @isemailverified.setter
    def isemailverified(self, value):
        self.set_property('isemailverified', value)

    @property
    def isenabled(self):
        return self.get_property('isenabled')

    @isenabled.setter
    def isenabled(self, value):
        self.set_property('isenabled', value)

    @property
    def isonline(self):
        return self.get_property('isonline')

    @isonline.setter
    def isonline(self, value):
        self.set_property('isonline', value)

    @property
    def connectionid(self):
        return self.get_property('connectionid')

    @connectionid.setter
    def connectionid(self, value):
        self.set_property('connectionid', value)

    @property
    def secretquestion(self):
        return self.get_property('secretquestion')

    @secretquestion.setter
    def secretquestion(self, value):
        self.set_property('secretquestion', value)

    @property
    def secretanswer(self):
        return self.get_property('secretanswer')

    @secretanswer.setter
    def secretanswer(self, value):
        self.set_property('secretanswer', value)

    @property
    def password(self):
        return self.get_property('password')

    @password.setter
    def password(self, value):
        self.set_property('password', value)

    @property
    def phone(self):
        return self.get_property('phone')

    @phone.setter
    def phone(self, value):
        self.set_property('phone', value)

    def create(self):
        mandatory_fields = ['username', 'email', 'firstname', 'password']
        for field in mandatory_fields:
            if self.__getattribute__(field) is None:
                raise ValidationError('{0} is a mandatory field.'.format(field))

        resp = super(AppacitiveUser, self).create()
        self.__set_self(resp['user'])

    @classmethod
    @user_auth_required
    def get_by_id(cls, user_id):

        if user_id is None:
            raise ValidationError('User id is missing.')

        url = urlfactory.user_urls["get"]('user', user_id)

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.get(url, headers)

        if response['status']['code'] != '200':
            return None

        return cls(response['user'])

    @classmethod
    @user_auth_required
    def get_by_username(cls, username):

        if username is None:
            raise ValidationError('Username is missing.')

        url = urlfactory.user_urls["get"]('user', username, 'username')

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.get(url, headers)

        if response['status']['code'] != '200':
            return None

        return cls(response['user'])

    @classmethod
    @user_auth_required
    def get_logged_in_user(cls):

        url = urlfactory.user_urls["get"]('user', 'me', 'token')

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.get(url, headers)

        if response['status']['code'] != '200':
            return None

        return cls(response['user'])

    @classmethod
    def authenticate(cls, username, password, expiry=None, attempts=None):

        url = urlfactory.user_urls['authenticate']()
        headers = urlfactory.get_headers()
        payload = {
            'username': username,
            'password': password
        }
        if expiry is not None:
            payload['expiry'] = expiry
        if attempts is not None:
            payload['attempts'] = attempts

        response = http.post(url, headers, json.dumps(payload))
        if response is not None and response['status']['code'] == '200':
            appcontext.ApplicationContext.set_user_token(response['token'])
            user = cls(response['user'])
            appcontext.ApplicationContext.set_logged_in_user(user)
            return user
        return None

    @classmethod
    def multi_get(cls, user_ids):
        response = AppacitiveObject.multi_get('user', user_ids)
        users = []
        for user in response['users']:
            user1 = cls(user)
            users.append(user1)
        return users

    @classmethod
    @user_auth_required
    def delete_by_id(cls, user_id, delete_connections=False):

        if user_id is None:
            raise ValidationError('User id is missing.')

        url = urlfactory.user_urls["delete"]('user', user_id, delete_connections)

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.delete(url, headers)

        if response['status']['code'] != '200':
            return None

    @classmethod
    @user_auth_required
    def delete_by_username(cls, username, delete_connections=False):

        if username is None:
            raise ValidationError('Username is missing.')

        url = urlfactory.user_urls["delete"]('user', username, 'username', delete_connections)

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.delete(url, headers)

        if response['status']['code'] != '200':
            return None

    @classmethod
    @user_auth_required
    def delete_logged_in_user(cls, delete_connections=False):

        url = urlfactory.user_urls["delete"]('user', 'me', 'token', delete_connections)

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.delete(url, headers)

        if response['status']['code'] != '200':
            return None

    def delete(self, delete_connections=False):
        return AppacitiveUser.delete_by_id(self.id, delete_connections)

    @user_auth_required
    def update(self):
        if self.type is None and self.type_id <= 0:
            raise ValidationError('Provide at least one among type name or type id.')

        if self.id <= 0:
            raise ValidationError('User id is missing.')

        url = urlfactory.user_urls["update"](self.id)
        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        payload = self.get_update_command()
        response = http.post(url, headers, payload)
        if response['status']['code'] != '200':
            return None

        user = response.get('user', None)
        if user is None:
            return response

        self.__set_self(user)

    @user_auth_required
    def update_password(self, old_password, new_password):

        url = urlfactory.user_urls["update_password"](self.id)

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        data = {
            "oldpassword": old_password,
            "newpassword": new_password
        }

        json_payload = json.dumps(data)
        response = http.post(url, headers, json_payload)
        if response['status']['code'] != '200':
            return None

    @staticmethod
    def send_reset_password_email(username, email_subject):

        url = urlfactory.user_urls["send_reset_password_email"]()
        headers = urlfactory.get_headers()

        data = {
            "username": username,
            "subject": email_subject
        }

        json_payload = json.dumps(data)
        response = http.post(url, headers, json_payload)
        if response['status']['code'] != '200':
            return None

    @staticmethod
    @user_auth_required
    def validate_session():
        url = urlfactory.user_urls["validate_session"]()
        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()
        payload = {}

        response = http.post(url, headers, json.dumps(payload))
        if response['status']['code'] != '200':
            return None
        return response['result']

    @staticmethod
    @user_auth_required
    def invalidate_session():
        url = urlfactory.user_urls["invalidate_session"]()
        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()
        payload = {}

        response = http.post(url, headers, json.dumps(payload))
        if response['status']['code'] != '200':
            return None
        return response['result']

    @user_auth_required
    def checkin(self, latitude, longitude):
        url = urlfactory.user_urls["checkin"](self.id, latitude, longitude)
        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()
        payload = {}

        response = http.post(url, headers, json.dumps(payload))
        if response['status']['code'] != '200':
            return None

    @classmethod
    @user_auth_required
    def find(cls, query):

        url = urlfactory.user_urls["find_all"](query)

        headers = urlfactory.get_headers()
        headers[AppacitiveUser.user_auth_header_key] = appcontext.ApplicationContext.get_user_token()

        response = http.get(url, headers)
        if response['status']['code'] != '200':
            return None

        users = response.get('users', None)
        if users is None:
            return response

        return_users = []
        for user in users:
            user1 = cls(user)
            return_users.append(user1)
        return return_users

