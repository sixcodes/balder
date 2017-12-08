from time import sleep
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

from models import Book


def save_book(book_dict):
    print(book_dict)
    b = Book(**book_dict)
    b.save()


def parse_table_to_dict(browser):
    table_rows = browser.find_by_css('td.td1')
    book_dict = {
        'library': 'Dedalus'
    }

    def parse_field(index, row_name, field, value):
        row_field = table_rows[index - 1].value
        if row_name in row_field:
            print('%s => %s' % (row_field, value))
            book_dict[field] = str(value)

    for index, row in enumerate(table_rows):
        if index > 0 and index % 2 is not 0:
            parse_field(index, 'ISBN', 'isbn', row.value)
            parse_field(index, 'Título', 'name', row.value)
            parse_field(index, 'No. Registro', 'call_number', row.value)
            parse_field(index, 'Entrada Principal', 'author', row.value)

    return book_dict


def select_first_book(browser):
    try:
        first_link = browser.find_by_css('.td1 > a')
        first_link.click()

        return True
    except ElementDoesNotExist as e:
        return False


def fill_fields_with_isbn(browser, term):
    browser.fill('request', term)
    browser.select('find_code', 'ISBN')

    search_button = browser.find_by_css('tr > td > input[type=image]').first
    search_button.click()


def enter_and_check_login(browser):
    browser.visit(
        'http://dedalus.usp.br/F/75Q3QI5IM28UTXP2NTCEHKXPJAAG2NY6KCE4G7AAMYLRC44QY3-16322'
    )

    if browser.find_by_css('a.lablebold').first:
        cancel_button = browser.find_by_css('input[value="Cancel"]').first
        cancel_button.click()


def crawl_dedalus(term):
    with Browser('chrome') as browser:
        enter_and_check_login(browser)
        fill_fields_with_isbn(browser, term)
        print('Searching for book...')

        sleep(2)

        if select_first_book(browser):
            print('The book was found!')

            sleep(2)

            book_data = parse_table_to_dict(browser)
            save_book(book_data)
            print('Book saved!')
        else:
            print('The book was not found...')
