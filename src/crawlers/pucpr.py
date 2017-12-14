from splinter import Browser
from models import Book
from datasource import DBConnection
from time import sleep
from threading import Thread
from errors import NoBookFoundError
import re

__all__ = (
    'crawl_pucpr',
)


def scroll_down(browser):
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")


def parse_table_to_dict(table, browser):
    have_isbn = False
    book_dict = {}

    def key_condition(string, row, key):
        if string in row.value:
            if key == 'isbn':
                book_dict[key] = re.search('((\d+-)+\d)', row.value.split('\n')[1]).group(0)
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

    close_modal_button = browser.find_by_text('Close (X)')
    close_modal_button.click()

    scroll_down(browser)
    scroll_down(browser)

    if have_isbn:
        return book_dict

    return False


def save_book_data(book_dict):
    try:
        b = Book(**book_dict)
        b.save()
    except Exception as e:
        print('LIVRO NÃO PODE SER SALVO! {}'.format(e))


def fill_search_bar(browser, term):
    browser.visit('http://www.biblioteca.pucpr.br/pergamum/biblioteca/pesquisa_avancada.php')
    browser.fill('termo_para_pesquisa1', term)
    select_field = browser.find_by_css('select.pmu_campo4')[0]

    browser.select('n_registros_por_pagina', '50')

    button = browser.find_by_name('pesq')

    button.click()


def crawl_pucpr(term):
    page_quantity = 50

    with Browser('chrome') as browser:
        fill_search_bar(browser, term)
