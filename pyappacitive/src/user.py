__author__ = 'sathley'

from object import AppacitiveObject as Base
from utilities import urlfactory, http, settings
import json

class User(Base):
    """
    The User object will provide the method to perform the user operations.
    user_obj.get(userid) will create the user
    """

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
