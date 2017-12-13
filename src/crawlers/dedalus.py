from time import sleep
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

from models import Book

__all__ = (
    'crawl_dedalus',
)


def save_book(book_dict):
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
            book_dict[field] = str(value)

    for index, row in enumerate(table_rows):
        if index > 0 and index % 2 is not 0:
            parse_field(index, 'ISBN', 'isbn', row.value)
            parse_field(index, 'Título', 'name', row.value)
            parse_field(index, 'Entrada Principal', 'author', row.value)
            parse_field(index, 'Imprenta', 'place', row.value)
            parse_field(index, 'Imprenta', 'year', row.value)

    return book_dict


def select_first_book(browser):
    try:
        first_link = browser.find_by_css('.td1 > a')
        first_link.click()

        return True
    except ElementDoesNotExist as err:
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
    crawler_name = 'Dedalus Crawler'
    with Browser('chrome') as browser:
        print('{}: Checking logind page'.format(crawler_name))
        enter_and_check_login(browser)
        print('{}: finding isbn...'.format(crawler_name))
        fill_fields_with_isbn(browser, term)
        print('{}: Searching for book...'.format(crawler_name))

        sleep(2)

        if select_first_book(browser):
            print('{}: The book was found!'.format(crawler_name))

            sleep(2)

            print('{}: Parsing book data'.format(crawler_name))
            book_data = parse_table_to_dict(browser)
            print('{}: Saving book data'.format(crawler_name))
            print('{}: {}'.format(crawler_name, book_data))
            save_book(book_data)
            print('{}: Book saved!'.format(crawler_name))
        else:
            print('{}: The book was not found...'.format(crawler_name))
