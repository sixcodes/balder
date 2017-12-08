from splinter import Browser
from time import sleep
from models import Book


def save_book(book_dict):
    pass


def parse_table_to_dict(browser):
    table_rows = browser.find_by_css('td.td1')
    for row in table_rows:
        print(row.value)


def select_first_book(browser):
    first_link = browser.find_by_css('.td1 > a')
    first_link.click()


def fill_fields_with_isbn(browser):
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
        fill_fields_with_isbn(browser)

        print('Searching for book...')

        sleep(2)

        select_first_book(browser)

        sleep(2)

        parse_table_to_dict(browser)


if __name__ == '__main__':
    crawl_dedalus('9788547302177')
