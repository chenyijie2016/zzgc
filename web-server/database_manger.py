from pymongo import MongoClient
import random

client = MongoClient()
db = client.zzgc  # database name: zzgc


def insert_device(device):
    collection = db.devices
    collection.insert_one(device)


def update_device(name, number):
    collection = db.devices
    collection.update_one({"Name": name}, {
        "$set": {"RemainingNumber": number}})


def insert_admin():
    collection = db.user
    collection.insert_one({"username": "super", "password": "pbkdf2:sha256:50000$jfmoS8be$cf3123b6e28aae3e83fcfc070233c984c90c2d4a25fb7be2b6841b874c928fb1", "email": "none", "authority": "admin"})


def set_default():
    devices = [
        {
            "Name": "Device 1",
            "Description": "Device 1 Description",
            "RemainingNumber": 0
        },
        {
            "Name": "Device 2",
            "Description": "Device 2 Description",
            "RemainingNumber": 0
        },
        {
            "Name": "Device 3",
            "Description": "Device 3 Description",
            "RemainingNumber": 0
        }
    ]
    for device in devices:
        insert_device(device)


def reset_device_number():
    devices = db.devices.find()
    for device in devices:
        update_device(device["Name"], random.randrange(0, 10))


if __name__ == '__main__':
    print('''
    [1]:set_default
    [2]:reset_device_number
    [3]:insert admin
    ''')

    option = input("Input option:")
    if option == '1':
        print('set_default')
        set_default()

    if option == '2':
        print('reset_device_number')
        reset_device_number()

    if option == '3':
        print('insert admin')
        insert_admin()