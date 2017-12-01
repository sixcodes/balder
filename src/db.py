from pymongo import MongoClient
from importlib import util
from configs.db import DB_HOST, DB_PORT


class DBClient(object):
    db_client = None

    @classmethod
    def client_instance(cls):
        if cls.db_client == None:
            cls.db_client = MongoClient(host=DB_HOST, port=DB_PORT)
        return cls.db_client


class Book(object):

    def __init__(self, name, isbn):
        self.name = name
        self.isbn = isbn

    def save(self):
        book = {
            'name': self.name,
            'isbn': self.isbn
        }
        book_col = self.__database().books
        try:
            return book_col.insert_one(book).inserted_id
        except Exception as e:
            return print('An error has ocurred! {}'.format(e))

    def __database(self):
        return DBClient.client_instance().library


def test_db_connection():
    b = Book(name='Pequeno Principe', isbn='04989489913413466')
    b.save()


if __name__ == '__main__':
    test_db_connection()
