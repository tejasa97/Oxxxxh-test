import logging
import os
import time
from time import gmtime, strftime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "localhost")


class AuditLoggingHandler(logging.Handler):

    log_type = "audit"

    def __init__(self, database, collection="mongolog"):
        logging.Handler.__init__(self)
        self.client = MongoClient(MONGO_URL)

        self.db = self.client[database]
        self.collection = self.db[collection]

    def emit(self, record):
        """save log record in file or database"""
        formatted_message = self.format(record)

        database_record = {
            "level": record.levelname,
            "type": self.log_type,
            "module": record.module,
            "asctime": record.asctime if getattr(record, "asctime", None) else strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "message": record.message  # use `formatted_message` for store formatted log
        }

        try:
            self.collection.insert_one(database_record)
        except Exception as e:
            print(e)


class AccessLoggingHandler(AuditLoggingHandler):
    log_type = "access"


class ActionLoggingHandler(AuditLoggingHandler):
    log_type = "action"


class FilterLevels(logging.Filter):
    def __init__(self, filter_levels=None):
        super(FilterLevels, self).__init__()
        self._filter_levels = filter_levels

    def filter(self, record):
        if record.levelname in self._filter_levels:
            return True
        return False
