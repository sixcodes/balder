from splinter import Browser
from models import Book
from time import sleep
from threading import Thread
import re


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

    links_list = browser.find_by_text('Fechar (X)')
    links_list[-1].click()

    scroll_down(browser)
    scroll_down(browser)

    if have_isbn:
        return book_dict

    return False


def save_book_data(book_dict):
    try:
        b = Book(**book_dict)
        b.save()
    except Exception:
        print('LIVRO NÃO PODE SER SALVO!')


def navigate_between_links(browser, links):
    window_initial_position = 0

    for link in links:
        if '( Livros )' in link.value:
            print(link.value)
            link.click()

            sleep(2)

            book_dict = parse_table_to_dict(browser.find_by_tag('table'), browser)

            if type(book_dict) is dict:
                print('================== SAVING BOOK ==================')
                save_book_data(book_dict)

            window_initial_position += 400
            browser.execute_script('window.scroll(0, {})'.format(window_initial_position))

            sleep(3)


def crawl_pucpr():
    with Browser('chrome') as browser:
        browser.visit('http://www.biblioteca.pucpr.br/pergamum/biblioteca/pesquisa_avancada.php')
        browser.fill('termo_para_pesquisa1', 'principe')
        browser.select('n_registros_por_pagina', '50')

        button = browser.find_by_name('pesq')

        button.click()

        sleep(5)

        print('Procurando por links...')
        page_quantity = int(browser.find_by_css('.txt_acervo2')[-1].value.split('-')[1])

        for page in range(page_quantity):
            links = browser.find_by_css('a.link_azul')

            navigate_between_links(browser, links)

            next_page = browser.find_by_css('a.pmu_paginacao2')[-1]
            next_page.click()

            sleep(5)


if __name__ == '__main__':
    crawl_pucpr()
