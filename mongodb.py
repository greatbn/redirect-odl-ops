import config

from pymongo import MongoClient
from bson import json_util
import json

class MongoDBWrapper(object):

    def __init__(self):
        conn = MongoClient(host=config.MONGODB_HOST,
                           port=config.MONGODB_PORT,
                           username=config.MONGODB_DB_USERNAME,
                           password=config.MONGODB_DB_PASSWORD)
        self.db = conn[config.MONGODB_DB_NAME]


    def save_flow(self, data):
        try:
            self.db.flows.save(data)
            return True
        except Exception as e:
            print("Something went wrong!!! {}".format(str(e)))
            return False

    def find_flow(self, data):
        try:
            return self.db.flows.find_one(data)
        except Exception as e:
            print("Something went wrong!!! {}".format(str(e)))
            return False

    def delete_flow(self, data):
        try:
            self.db.flows.delete_one(data)
            return True
        except Exception as e:
            print("Something went wrong!!! {}".format(str(e)))
            return False

    def update_flow(self, filter, data):
        try:
            self.db.flows.update(filter, data)
            return True
        except Exception as e:
            return False

    def list_flows(self):

        try:
            return json.loads(json_util.dumps(list(self.db.flows.find({}))))
        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":
    
    db = MongoDBWrapper()
    db.delete_flow({'attacker_ip': '192.168.110.186', 'victim_ip': '192.168.110.181'})
