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
    collection.insert_one({"username": "admin", "password": "admin", "email": "none", "authority": "admin"})


if __name__ == '__main__':
    devices = db.devices.find()
    for device in devices:
        update_device(device["Name"], random.randrange(0, 10))
