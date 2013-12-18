__author__ = 'sathley'

from object import AppacitiveObject
from utilities import urlfactory, http, settings
from error import ValidationError
import json


class AppacitiveUser(AppacitiveObject):

    def __init__(self):
        super(AppacitiveUser, self).__init__()
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

#region          user properties
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
#endregion

    def create(self):
        mandatory_fields = ['username', 'email', 'firstname', 'password']
        for field in mandatory_fields:
            if self.__getattribute__(field) is None:
                raise ValidationError('{0} is a mandatory field.'.format(field))

        return super(AppacitiveUser, self).create()



























    def update_password(self, identification_type, old_password, new_password):
        """
        Method will update the password
        Input: user object to update the password, old_password and new_password
        """
        if self.id <= 0 or identification_type not in ('id', 'username',
                                                       'token'):
            raise ValueError('Incorrect data.')

        url = urlfactory.user_urls["update_password"](
            self.id, identification_type)
        # Converted it to a dict manually because the header key
        # Appacitive-User-Auth was not accepted as argument. But the set_headers
        # should be the same. As every arguments may not be the same

        headers = urlfactory.get_headers(**{"Appacitive-User-Auth": self.token})
        data = {"oldpassword": old_password,
                "newpassword": new_password}
        json_payload = json.dumps(data)
        return http.post(url, headers, json_payload)
