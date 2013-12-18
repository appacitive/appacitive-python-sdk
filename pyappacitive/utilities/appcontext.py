__author__ = 'sathley'


class ApplicationContext(object):
    def __init__(self):
        pass

    logged_in_user = None

    user_token = None

    @staticmethod
    def get_logged_in_user():
        return ApplicationContext.logged_in_user

    @staticmethod
    def get_user_token():
        return ApplicationContext.user_token

    @staticmethod
    def set_logged_in_user(user):
        ApplicationContext.logged_in_user = user

    @staticmethod
    def set_user_token(token):
        ApplicationContext.user_token = token


