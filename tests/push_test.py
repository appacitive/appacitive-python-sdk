__author__ = 'sathley'

from pyappacitive import AppacitivePushNotification


def send_push_notification_test():
    response = AppacitivePushNotification.broadcast(data={'alert': 'hi from py sdk'})
    assert response.status.code == '200'
    assert hasattr(response, 'id')
    assert response.id is not None and response.id > 0


def get_all_notifications_test():
    response = AppacitivePushNotification.get_all_notification()
    assert response.status.code == '200'
    assert hasattr(response, 'notifications')
    assert len(response.notifications) > 0


def get_notification_by_id_test():
    response = AppacitivePushNotification.broadcast(data={'alert': 'hi from py sdk'})
    id = response.id
    response = AppacitivePushNotification.get_notification_by_id(id)
    assert response.status.code == '200'
    assert hasattr(response, 'notification')
    assert response.notification is not None
    assert response.notification.id == id