from splinter import Browser
from time import sleep


def parse_table_to_dict(table_element):
    print(table_element[0])


def select_first(browser):
    first_link = browser.find_by_css('.td1 > a')
    first_link.click()


def crawl_dedalus(term):
    with Browser('chrome') as browser:
        browser.visit(
            'http://dedalus.usp.br/F/75Q3QI5IM28UTXP2NTCEHKXPJAAG2NY6KCE4G7AAMYLRC44QY3-16322'
        )
        browser.fill('request', term)
        browser.select('find_code', 'ISBN')

        search_button = browser.find_by_css('tr > td > input[type=image]')
        search_button.click()
        print('Searching for book...')

        sleep(5)

        select_first(browser)

        sleep(5)

        table = browser.find_by_css('table')
        parse_table_to_dict(table)


if __name__ == '__main__':
    crawl_dedalus('9788547302177')
