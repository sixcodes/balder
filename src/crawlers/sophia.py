from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


from errors import NoBookFoundError
from models import Book

__all__ = (
    'crawl_sophia',
)


def save_book(book):
    b = Book(**book)
    b.save()


def extract_book_data_as_dict(driver):
    book_fields = driver.find_elements_by_css_selector('td.td_detalhe_descricao')
    book_data = driver.find_elements_by_css_selector('td.td_detalhe_valor')
    book_dict = {}

    def parse_field(index, row_name, field):
        if row_name in book_fields[index - 1].text:
            book_dict[field] = book_data[index].text

    for key, field in enumerate(book_fields):
        parse_field(key, 'ISBN', 'isbn')
        parse_field(key, 'Título', 'name')
        parse_field(key, 'Ent. princ.', 'author')
        parse_field(key, 'Assuntos', 'place')
        parse_field(key, 'Imprenta', 'year')
        parse_field(key, 'Edição', 'publisher')

    book_dict['library'] = 'sophia'
    print(book_dict)

    return book_dict


def take_book_on_list(driver):
    books_list = driver.find_element_by_css_selector(
        'table.max_width'
    )
    if books_list:
        book_link = driver.find_elements_by_css_selector(
            'td#s_det1600665.esquerda.td_ficha_serv'
        )
        book_link[0].click()
        sleep(3)
    else:
        raise NoBookFoundError


def find_by_isbn(driver, isbn):
    search_field = driver.find_element_by_css_selector('.input_busca')
    search_field.send_keys(isbn)

    driver.find_elements_by_css_selector(
        'button.ui-multiselect.ui-widget.ui-state-default.ui-corner-all'
    )[2].click()

    driver.find_element_by_css_selector(
        'label[for="ui-multiselect-rapida_filtro-option-5"]'
    ).click()

    driver.find_elements_by_css_selector(
        'input[value="Buscar"]'
    )[0].click()

    sleep(3)


def find_iframe(driver):
    iframe = driver.find_element_by_id('mainFrame')
    driver.switch_to_frame(iframe)


def crawl_sophia(term):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        driver.get('http://acervo.bn.br/sophia_web/index.html')
        print('Sophia Crawler: Finding iframe...')
        find_iframe(driver)
        print('Sophia Crawler: Searching book by isbn...')
        find_by_isbn(driver, term)
        print('Sophia Crawler: Taking the first book of the list')
        take_book_on_list(driver)
        print('Sophia Crawler: Extracting book data...')
        book_dict = extract_book_data_as_dict(driver)

        print('Sophia Crawler: Saving book...')
        save_book(book_dict)

        print('Sophia Crawler: Book was saved!')

        driver.close()

    except NoBookFoundError as e:
        print('Sophia Crawler: No book found!')

    except Exception as e:
        print(e)
        driver.close()
