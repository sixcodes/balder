from splinter import Browser
from selenium import webdriver
from time import sleep


def crawl_one(browser, term):
    browser.fill('rapida_campo', term)
    search_button = browser.find_by_css('.button_busca')[0]
    search_button.click()
    sleep(3)

    browser.find_by_css('input.input_busca')


def crawl_list(browser, term):
    pass


def crawl_sophia():
    with Browser('chrome') as browser:
        browser.visit('http://acervo.bn.br/sophia_web/index.html')
        crawl_one(browser, '8528102246')


if __name__ == '__main__':
    crawl_sophia()
