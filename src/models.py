import datasource


class Book(datasource.Model):

    database = 'balder'
    collection = 'books'

    name = datasource.StringFiled('name', default_value='')
    isbn = datasource.StringFiled('isbn', default_value='')
    author = datasource.StringFiled('author', default_value='')
    main_title = datasource.StringFiled('mainTitle', default_value='')
    general_notes = datasource.StringFiled('generalNotes', default_value='')

    def __init__(self, *args, **kwargs):
        self.set_unique_key('isbn')


def test_db_connection():
    b = Book(name='Pequeno Teste 876', isbn='99729839128371273123',
             author='Teste author', main_title='QUlauqer',
             general_notes='qualquer uma')
    b.save()

    # print(Book.get_by(key='isbn', value='8479283479234'))


if __name__ == '__main__':
    test_db_connection()
