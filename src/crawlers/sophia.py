from splinter import Browser
from selenium import webdriver
from time import sleep


__all__ = (
    'crawl_sophia',
)


def find_by_isbn(driver, isbn):
    search_field = driver.find_element_by_css_selector('.input_busca')
    search_field.send_keys(isbn)

    driver.find_elements_by_css_selector(
        'button.ui-multiselect.ui-widget.ui-state-default.ui-corner-all'
    )[2].click()

    driver.find_element_by_css_selector(
        'label[for="ui-multiselect-rapida_filtro-option-5"]'
    ).click()

    sleep(5)


def find_iframe(driver):
    iframe = driver.find_element_by_id('mainFrame')
    driver.switch_to_frame(iframe)


def crawl_sophia(term):
    driver = webdriver.Chrome()

    try:
        driver.get('http://acervo.bn.br/sophia_web/index.html')
        find_iframe(driver)
        find_by_isbn(driver, term)

        driver.close()
    except Exception as e:
        print(e)
        driver.close()
