from pymongo import MongoClient, ASCENDING
from importlib import util
from configs.db import DB_HOST, DB_PORT


class DBClient(object):

    db_client = None

    @classmethod
    def db_instance(cls, database):
        if cls.db_client == None:
            cls.db_client = MongoClient(host=DB_HOST, port=DB_PORT)
        return cls.db_client[database]


class QueryError(Exception):
    pass


class Model(object):

    database = 'default'
    collection = 'default'
    _id = 'default'

    def __new__(cls, *args, **kwargs):
        instance = super(Model, cls).__new__(cls)
        instance.__dict__ = kwargs
        return instance

    @classmethod
    def collection_instance(cls):
        return DBClient.db_instance(cls.database)[cls.collection]

    @classmethod
    def set_unique_key(cls, key):
        index_dict = cls.collection_instance().index_information()

        if not '{}_1'.format(key) in index_dict:
            cls.collection.create_index([(key, ASCENDING)], unique=True)

    def save(self):
        new_doc = self.__dict__
        try:
            return self.collection_instance().insert_one(new_doc).inserted_id
        except Exception as e:
            raise QueryError()
            # return print('An error has ocurred! {}'.format(e))

    @classmethod
    def get_by(cls, key, value):
        try:
            return cls.collection_instance().find({key: value})[0]
        except Exception as e:
            raise QueryError()
            # return print('An error has ocurred! {}'.format(e))

    @classmethod
    def get_all(cls):
        try:
            return cls.collection_instance().find({})
        except Exception as e:
            raise QueryError()
            # return print('An error has ocurred! {}'.format(e))


class BaseField(object):
    pass
    # def __init__(self,  unique=False):
    #     pass


class StringFiled(BaseField):
    def __new__(cls, field_name, default_value):
        if not default_value:
            return ''

        return default_value
        

class NumberFiled(BaseField):
    def __new__(cls, field_name, default_value):
        if not default_value:
            return 0

        return default_value


class ObjectFiled(BaseField):
    def __new__(cls, field_name, default_value):
        if not default_value:
            return object()

        return default_value
