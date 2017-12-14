import re
from time import sleep
from threading import Thread

from splinter import Browser
from models import Book
from datasource import DBConnection
from errors import NoBookFoundError

__all__ = (
    'crawl_pucpr',
)


def save_book_data(book_dict):
    try:
        b = Book(**book_dict)
        b.save()
    except Exception as e:
        print('Book cannot be saved! {}'.format(e))


def scroll_down(browser):
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")


def parse_table_to_dict(table, browser):
    have_isbn = False
    book_dict = {'library': 'Pucpr'}

    def key_condition(string, row, key):
        if string in row.value:
            if key == 'isbn':
                book_dict[key] = re.search(
                    '((\d+-)+\d)', row.value.split('\n')[1]).group(0).replace('-', '')
            else:
                book_dict[key] = row.value.split('\n')[1]

    for row in table:
        if 'Número Normalizado' in row.value:
            have_isbn = True

        row_data = row.value.split('\n')

        key_condition('Número Normalizado', row, 'isbn')
        key_condition('Título Principal', row, 'name')
        key_condition('Autor', row, 'author')

        if 'Assuntos' in row.value:
            break

    if have_isbn:
        return book_dict

    return False


def get_table(browser):
    return browser.find_by_css('table[width="95%"]')


def clicking_on_first_link(browser):
    link_tags = browser.find_by_css('tr[align="left"] > td > a.link_azul')

    if len(link_tags) != 0:
        link_tags[0].click()
    else:
        raise NoBookFoundError


def fill_search_bar(browser, term):
    browser.fill('termo_para_pesquisa1', term)
    # clicking on select and search button
    browser.find_by_css('select#filtro1.pmu_campo4')[0].click()
    browser.find_by_css('option[value="LIVRE"]')[0].click()

    browser.find_by_css('input#fs.pmu_btn11')[0].click()


def crawl_pucpr(term):
    page_quantity = 50
    crawler_name = 'Pucpr crawler'

    with Browser('chrome', headless=True) as browser:
        browser.visit('http://www.biblioteca.pucpr.br/pergamum/biblioteca/pesquisa_avancada.php')
        browser.driver.set_window_size(800, 600)

        print('%s: Searching by isbn' % crawler_name)
        fill_search_bar(browser, term)

        try:
            clicking_on_first_link(browser)
            print('%s: The book was found!' % crawler_name)
            print('%s: Getting book from table' % crawler_name)
            table = get_table(browser)
            print('%s: Parsing book data' % crawler_name)
            book = parse_table_to_dict(table, browser)
            print(book)

            print('%s: Saving book data' % crawler_name)
            save_book_data(book)

            print('%s: Book was saved!' % crawler_name)

        except NoBookFoundError as error:
            print('%s: No book found...' % crawler_name)

        except Exception as error:
            print(error)
            print('An error has occured...')
