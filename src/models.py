from mongoengine import Document, StringField
from datasource import DBConnection


class Book(Document):

    isbn = StringField(default='', unique=True)
    name = StringField(default='')
    call_number = StringField(default='')
    subject = StringField(default='')
    author = StringField(default='')
    main_title = StringField(default='')
    general_notes = StringField(default='')


def test_db_connection():
    DBConnection()
    b = Book(name='Pequeno Teste 4567', isbn='9840283048234',
             author='Teste author', main_title='QUlauqer',
             general_notes='qualquer uma')
    b.save()
    # print(Book.get_by(key='isbn', value='8479283479234'))


if __name__ == '__main__':
    test_db_connection()
