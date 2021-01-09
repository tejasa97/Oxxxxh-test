from enum import Enum
from db_clients.mongodb import MongoConnection

MONGO_LOGS_COLLECTION = 'logs'


class MongoLogsClient():

    class LogType(Enum):

        ACCESS = 'access'
        ACTION = 'action'
        AUDIT = 'audit'

        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_

    def __init__(self, client=MongoConnection()):
        self.client = client

    def get_logs(self, log_type=None):
        """Returns all logs
        :return: JSON
        """

        if log_type is None:
            conn = self.client.get_collection(MONGO_LOGS_COLLECTION)
            return list(conn.find({}, {'_id': 0, 'type': 1, 'message': 1, 'asctime': 1}))

        if self.LogType.has_value(log_type) is False:
            raise Exception("Invalid log type")

        conn = self.client.get_collection(MONGO_LOGS_COLLECTION)
        return list(conn.find({"type": log_type}, {'_id': 0, 'message': 1, 'asctime': 1}))
