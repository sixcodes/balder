import mongoengine
from configs.db import DB_HOST, DB_PORT, DB_NAME


class DBConnection(object):

    connection = None

    def __new__(cls):
        if cls.connection == None:
            cls.connection = mongoengine.connect(
                db=DB_NAME, host=DB_HOST, port=DB_PORT
            )
        return cls.connection
