from splinter import Browser
from models import Book
from datasource import DBConnection
from time import sleep
from threading import Thread
import re


DBConnection()


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

        key_condition('Autor', row, 'author')
        key_condition('Título Principal', row, 'main_title')
        key_condition('Título Uniforme', row, 'title')
        key_condition('Número de Chamada', row, 'call_number')
        key_condition('Número Normalizado', row, 'isbn')
        key_condition('Notas Gerais', row, 'general_notes')
        key_condition('Assuntos', row, 'subject')

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


def navigate_between_links(browser, links):
    window_initial_position = 0

    for link in links:
        if '( Livros )' in link.value:
            window_initial_position += 400
            browser.execute_script('window.scroll(0, {})'.format(window_initial_position))

            print(link.value)
            link.click()

            sleep(6)

            book_dict = parse_table_to_dict(browser.find_by_css('table'), browser)

            if type(book_dict) is dict:
                print('================== SAVING BOOK ==================')
                save_book_data(book_dict)

            sleep(3)


def crawl_pucpr(term):
    page_quantity = 50

    with Browser('chrome') as browser:
        browser.visit('http://www.biblioteca.pucpr.br/pergamum/biblioteca/pesquisa_avancada.php')
        browser.fill('termo_para_pesquisa1', term)
        browser.select('n_registros_por_pagina', '50')

        button = browser.find_by_name('pesq')

        button.click()

        sleep(5)

        print('Procurando por links...')

        for page in range(page_quantity):
            sleep(50)
            links = browser.find_by_css('a.link_azul')

            navigate_between_links(browser, links)

            next_page = browser.find_by_text('Next »')[0]
            next_page.click()

            sleep(5)


if __name__ == '__main__':
    crawl_pucpr('principe')
    # threads = [Thread(target=crawl_pucpr, args=('laranja',)),
    #            Thread(target=crawl_pucpr, args=('principe',)),
    #            Thread(target=crawl_pucpr, args=('rouba',)),
    #            Thread(target=crawl_pucpr, args=('cabana',)),
    #            Thread(target=crawl_pucpr, args=('contos',))]

    # for t in threads:
    #     t.start()
