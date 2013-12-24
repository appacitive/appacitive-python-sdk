__author__ = 'sathley'

from pyappacitive import AppacitiveUser, AppacitiveQuery, PropertyFilter, UserAuthError, ApplicationContext
import random
import datetime
from nose.tools import *


def get_random_string(number_of_characters=10):
    arr = [str(i) for i in range(number_of_characters)]
    random.shuffle(arr)
    return ''.join(arr)


def get_random_number(number_of_digits=10):
    arr = [str(i) for i in range(number_of_digits)]
    random.shuffle(arr)
    return int(''.join(arr))


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
    assert resp.status.code == '200'
    assert user.id > 0


def get_user_by_id_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')
    resp = AppacitiveUser.get_by_id(user.id)
    assert resp.status.code == '200'
    assert hasattr(resp, 'user')
    assert user.id == resp.user.id


def get_user_by_username_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')
    resp = AppacitiveUser.get_by_username(user.username)
    assert resp.status.code == '200'
    assert hasattr(resp, 'user')
    assert user.id == resp.user.id


def get_logged_in_user_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')
    resp = AppacitiveUser.get_logged_in_user()
    assert hasattr(resp, 'user')
    assert user.id == resp.user.id


def multiget_user_test():
    user_ids = []
    for i in range(2):
        user = get_random_user()
        user.create()
        user_ids.append(user.id)
    user.authenticate('test123!@#')

    response = AppacitiveUser.multi_get(user_ids)
    assert response.status.code == '200'
    assert len(response.users) == 2


def delete_user_test():
    user = get_random_user()
    user.create()
    user_id = user.id
    user.authenticate('test123!@#')
    response = user.delete()
    assert response.status.code == '200'

    response = AppacitiveUser.get_by_id(user_id)
    assert response.status.code != '200'
    assert hasattr(response, 'user') is False


def delete_by_username_test():
    user = get_random_user()
    user.create()
    user_id = user.id
    user.authenticate('test123!@#')
    response = AppacitiveUser.delete_by_username(user.username)
    assert response.status.code == '200'

    response = AppacitiveUser.get_by_id(user_id)
    assert response.status.code != '200'
    assert hasattr(response, 'user') is False


def delete_logged_in_user_test():
    user = get_random_user()
    user.create()
    user_id = user.id
    user.authenticate('test123!@#')
    response = AppacitiveUser.delete_logged_in_user()
    assert response.status.code == '200'

    response = AppacitiveUser.get_by_id(user_id)
    assert response.status.code != '200'
    assert hasattr(response, 'user') is False


def update_user_test():
    user = get_random_user()
    user.set_attribute('a1', 'v1')
    user.set_attribute('a2', 'v2')
    user.add_tags(['t1', 't2', 't3]'])
    user.birthdate = datetime.date.today()
    user.lastname = 'LN'

    user.create()
    user.authenticate('test123!@#')

    user.remove_tag('t1')
    user.add_tag('t4')
    user.remove_attribute('a1')
    user.set_attribute('a3', 'v3')
    user.lastname = 'LN2'

    response = user.update()
    assert response.status.code == '200'
    assert user.tag_exists('t1') is False
    assert user.tag_exists('t4')
    assert user.get_attribute('a1') is None
    assert user.get_attribute('a3') == 'v3'
    assert user.lastname == 'LN2'


def update_password_user_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')

    response = user.update_password('test123!@#', 'zaq1ZAQ!')
    assert response.status.code == '200'

    response = user.authenticate('test123!@#')
    assert response.status.code != '200'

    response = user.authenticate('zaq1ZAQ!')
    assert response.status.code == '200'


def validate_session_user_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')

    response = AppacitiveUser.validate_session()
    assert response.status.code == '200'
    assert response.result is True

    response = AppacitiveUser.invalidate_session()
    assert response.status.code == '200'

    response = AppacitiveUser.validate_session()
    assert response.status.code != '200'


def checkin_user_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')

    response = user.checkin(10.10, 20.20)
    assert response.status.code == '200'

    user.fetch_latest()
    assert user.location == '10.1,20.2'


def find_user_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')
    query = AppacitiveQuery()
    query.filter = PropertyFilter('firstname').is_equal_to('Jon')
    response = AppacitiveUser.find(query)
    assert response.status.code == '200'
    assert hasattr(response,  'users')
    assert len(response.users) > 0


def authenticate_user_test():
    user = get_random_user()
    user.create()
    response = AppacitiveUser.authenticate_user(user.username, 'test123!@#')
    assert response.status.code == '200'
    assert response.user is not None
    assert response.user.id == user.id


@raises(UserAuthError)
def get_user_without_token_test():
    user = get_random_user()
    user.create()
    ApplicationContext.set_user_token(None)
    response = AppacitiveUser.get_by_username(user.username)
    assert response.status.code != '200'


def get_user_with_invalid_token_test():
    user = get_random_user()
    user.create()
    user.authenticate('test123!@#')
    AppacitiveUser.invalidate_session()
    response = AppacitiveUser.get_by_username(user.username)
    assert response.status.code != '200'