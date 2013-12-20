__author__ = 'sathley'

from pyappacitive import AppacitiveUser
import random
import datetime


def get_random_string():
    arr = [str(i) for i in range(10)]
    random.shuffle(arr)
    return ''.join(arr)


def get_random_user():
    user = AppacitiveUser()
    user.username = 'jon'+get_random_string()
    user.password = 'test123!@#'
    user.email = 'jon' + get_random_string() + '@gmail.com'
    user.firstname = 'Jon'
    return user


def create_user_test():
    user = get_random_user()

    user.birthdate = datetime.date.today()
    user.location = '10.10,20.20'
    user.connectionid = 100
    user.isemailverified = True
    user.isenabled = True
    user.isonline = False
    user.lastname = 'Doe'
    user.phone = '555-444-333'
    user.secretquestion = 'Favourite programming language?'
    user.secretanswer = 'python'

    resp = user.create()
    assert resp.status_code == '200'
    assert user.id > 0


def get_user_by_id_test():
    pass
    #user = get_random_user()
    #user.create()
    #resp = AppacitiveUser.get_by_id(user.id)
    #assert resp.status_code == '200'
    #assert hasattr(resp, 'user')
    #assert user.id == resp.user.id


def multiget_user_test():
    pass


def delete_user_test():
    pass


def update_user_test():
    pass


def update_password_user_test():
    pass


def validate_session_user_test():
    pass


def invalidate_session_user_test():
    pass


def checkin_user_test():
    pass


def authenticate_user_test():
    pass