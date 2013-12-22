__author__ = 'sathley'

from pyappacitive import AppacitiveDevice
import random
from pyappacitive import AppacitiveQuery, PropertyFilter


def get_random_string(number_of_characters=10):
    arr = [str(i) for i in range(number_of_characters)]
    random.shuffle(arr)
    return ''.join(arr)


def get_random_device():
    device = AppacitiveDevice()
    device.devicetype = 'ios'
    device.devicetoken = get_random_string()
    device.location = '10.10,20.20'
    return device


def register_device_test():
    device = get_random_device()
    response = device.register()
    assert response.status.code == '200'
    assert device.id > 0


def get_device_test():
    device = get_random_device()
    device.register()

    response = AppacitiveDevice.get(device.id)
    assert response.status.code == '200'
    assert hasattr(response, 'device')
    assert response.device is not None
    assert response.device.id == device.id


def multi_get_device_test():
    device_ids = []
    for i in range(12):
        device = get_random_device()
        device.register()
        device_ids.append(device.id)
    response = AppacitiveDevice.multi_get(device_ids)
    assert response.status.code == '200'
    assert hasattr(response, 'devices')
    assert len(response.devices) == 12


def device_update_test():
    device = get_random_device()
    device.badge = 100
    device.register()

    device.badge = 200
    response = device.update()
    assert response.status.code == '200'
    assert device.badge == 200


def delete_device_test():
    device = get_random_device()
    device.register()
    device_id = device.id
    response = device.delete()
    assert response.status.code == '200'

    response = AppacitiveDevice.get(device_id)
    assert response.status.code != '200'
    assert hasattr(response, 'device') is False


def find_device_test():
    device = get_random_device()
    device.register()
    query = AppacitiveQuery()
    query.filter = PropertyFilter.is_equal_to('devicetype', 'ios')
    response = AppacitiveDevice.find(query)
    assert response.status.code == '200'
    assert hasattr(response, 'devices')
    assert len(response.devices) > 0