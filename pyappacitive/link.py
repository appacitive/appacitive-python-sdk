__author__ = 'sathley'


class Link(object):
    def __init__(self, link):
        if link is not None:
            self.name = link.get('name', None)
            self.auth_type = link.get('authtype', None)
            self.username = link.get('username', None)

            for k, v in link.iteritems():
                if k not in ['name', 'authtype', 'username']:
                    self.__setattr__(k, v)