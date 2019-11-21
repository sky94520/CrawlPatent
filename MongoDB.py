import pymongo


class MongoDB(object):

    def __init__(self, host, port):
        self.mongo = pymongo.MongoClient(host=host, port=port)

    def authenticate(self, db_name, name, password):
        db = self.mongo[db_name]
        db.authenticate(name=name, password=password)

    def get_db(self, name):
        return self.mongo[name]
