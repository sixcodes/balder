from mongoengine import Document, StringField
from datasource import DBConnection


class Book(Document):

    isbn = StringField(default='', unique=True)
    name = StringField(default='')
    call_number = StringField(default=None)
    subject = StringField(default=None)
    author = StringField(default=None)
    main_title = StringField(default=None)
    general_notes = StringField(default=None)
    library = StringField(default=None)
