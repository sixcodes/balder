from splinter import Browser
from db import Book
from time import sleep
from threading import Thread


def parse_table_to_dict(table):
    attrs = [a for a in dir(table) if not a.startswith('__')]
    print(table.first.value)


def save_book_data():
    pass


def crawl_acervo_pucpr():
    with Browser('chrome') as browser:
        browser.visit('http://www.biblioteca.pucpr.br/pergamum/biblioteca/pesquisa_avancada.php')
        browser.fill('termo_para_pesquisa1', 'principe')
        button = browser.find_by_name('pesq')

        button.click()

        sleep(4)

        print('Procurando por links...')
        links = browser.find_by_css('.link_azul')

        for link in links:
            if '( Livros )' in link.value:
                print(link.value)
                link.click()

                sleep(2)

                parse_table_to_dict(browser.find_by_tag('table'))

                close_link = browser.find_by_id('fechar_2')
                close_link.click()


if __name__ == '__main__':
    crawl_acervo_pucpr()
