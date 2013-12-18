from pyappacitive.utilities import http, urlfactory

__author__ = 'sathley'

from pyappacitive.object import AppacitiveObject
from pyappacitive.entity import object_system_properties
from pyappacitive.error import ValidationError
import json


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

        resp = super(AppacitiveUser, self).create()
        self.__set_self(resp['user'])




























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
