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

    def __init__(self, obj=None):
        super(AppacitiveUser, self).__init__(obj)
        self._properties = {
            'username': None,
            'location': None,
            'email': None,
            'firstname': None,
            'lastname': None,
            'birthdate': None,
            'isemailverified': None,
            'isenabled': None,
            'isonline': None,
            'connectionid': None,
            'secretquestion': None,
            'secretanswer': None,
            'password': None,
            'phone': None
        }
        self.type = 'user'

    user_auth_header_key = 'Appacitive-User-Auth'

    def __set_self(self, obj):

        if obj is None:
            pass

        self.id = int(obj['__id']) if '__id' in obj else 0
        self.type = obj['__type'] if '__type' in obj else None
        self.type_id = int(obj['__typeid']) if '__typeid' in obj else 0
        self.created_by = obj['__createdby'] if '__createdby' in obj else None
        self.last_modified_by = obj['__lastmodifiedby'] if '__lastmodifiedby' in obj else None
        self.utc_date_created = obj['__utcdatecreated'] if '__utcdatecreated' in obj else None
        self.utc_last_updated_date = obj['__utclastupdateddate'] if '__utclastupdateddate' in obj else None
        self._tags = obj['__tags'] if '__tags' in obj else None
        self._attributes = obj['__attributes'] if '__attributes' in obj else None
        self.revision = int(obj['__revision']) if '__revision' in obj else None
        for k, v in obj.iteritems():
            if k not in object_system_properties:
                self._properties[k] = v


    @property
    def username(self):
        return self._properties['username']

    @username.setter
    def username(self, value):
        self._properties['username'] = value

    @property
    def location(self):
        return self._properties['location']

    @location.setter
    def location(self, value):
        self._properties['location'] = value

    @property
    def email(self):
        return self._properties['email']

    @email.setter
    def email(self, value):
        self._properties['email'] = value

    @property
    def firstname(self):
        return self._properties['firstname']

    @firstname.setter
    def firstname(self, value):
        self._properties['firstname'] = value

    @property
    def lastname(self):
        return self._properties['lastname']

    @lastname.setter
    def lastname(self, value):
        self._properties['lastname'] = value

    @property
    def birthdate(self):
        return self._properties['birthdate']

    @birthdate.setter
    def birthdate(self, value):
        self._properties['birthdate'] = value

    @property
    def isemailverified(self):
        return self._properties['isemailverified']

    @isemailverified.setter
    def isemailverified(self, value):
        self._properties['isemailverified'] = value

    @property
    def isenabled(self):
        return self._properties['isenabled']

    @isenabled.setter
    def isenabled(self, value):
        self._properties['isenabled'] = value

    @property
    def isonline(self):
        return self._properties['isonline']

    @isonline.setter
    def isonline(self, value):
        self._properties['isonline'] = value

    @property
    def connectionid(self):
        return self._properties['connectionid']

    @connectionid.setter
    def connectionid(self, value):
        self._properties['connectionid'] = value

    @property
    def secretquestion(self):
        return self._properties['secretquestion']

    @secretquestion.setter
    def secretquestion(self, value):
        self._properties['secretquestion'] = value

    @property
    def secretanswer(self):
        return self._properties['secretanswer']

    @secretanswer.setter
    def secretanswer(self, value):
        self._properties['secretanswer'] = value

    @property
    def password(self):
        return self._properties['password']

    @password.setter
    def password(self, value):
        self._properties['password'] = value

    @property
    def phone(self):
        return self._properties['phone']

    @phone.setter
    def phone(self, value):
        self._properties['phone'] = value

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

