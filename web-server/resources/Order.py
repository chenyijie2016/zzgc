from flask import current_app


class Order(object):
    def __init__(self):
        pass

    @staticmethod
    def find(username):
        db = current_app.config["database"]
        a = db.order.find_one({"username": username})
        if a:
            return True
        else:
            return False

    @staticmethod
    def add_user_order(username):
        db = current_app.config["database"]
        db.order.insert_one(
            {
                "username": username,
                "orders": []
            }
        )

    def set(self, username, devicename, number):
        db = current_app.config["database"]
        if not self.find(username):
            self.add_user_order(username)

