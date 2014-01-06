__author__ = 'sathley'

from pyappacitive import AppacitivePushNotification, PropertyFilter


def send_push_notification_test():
    response_id = AppacitivePushNotification.broadcast(data={'alert': 'hi from py sdk'})
    assert response_id is not None and response_id > 0


def get_all_notifications_test():
    notifications = AppacitivePushNotification.get_all_notification()
    assert len(notifications) > 0


def get_notification_by_id_test():
    notification_id = AppacitivePushNotification.broadcast(data={'alert': 'hi from py sdk'})
    notification = AppacitivePushNotification.get_notification_by_id(notification_id)
    assert notification is not None
    assert notification.id == notification_id


def send_push_notification_to_channels_test():
    response_id = AppacitivePushNotification.send_to_channels(['male', '18-25'], {'alert': 'Hi from pyAppacitive'}, platform_options={
		"ios": {
			"sound": "test"
		},
		"android": {
			"title": "test title"
		}
	})

    assert response_id is not None and response_id > 0


def send_push_notification_to_specific_devices_test():
    response_id = AppacitivePushNotification.send_to_specific_devices(['123', '456', '789'], {'alert': 'Hi from pyAppacitive'}, platform_options={
		"ios": {
			"sound": "test"
		},
		"android": {
			"title": "test title"
		}
	})

    assert response_id is not None and response_id > 0


def send_push_using_query_test():
    query = PropertyFilter('devicetype').is_equal_to('ios')
    response_id = AppacitivePushNotification.send_using_query(query, {'alert': 'Hi from pyAppacitive'}, platform_options={
		"ios": {
			"sound": "test"
		},
		"android": {
			"title": "test title"
		}
	})
    assert response_id is not None and response_id > 0