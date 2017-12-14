from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    book_dict = {'library': 'sophia'}

    def parse_field(index, row_name, field):
        if row_name in book_fields[index - 1].text:
            if field is 'isbn':
                book_dict[field] = book_data[index - 1].text \
                    .replace('.', '').replace(' ', '').replace('(broch)', '')
            else:
                book_dict[field] = book_data[index - 1].text

    for key, field in enumerate(book_fields):
        parse_field(key, 'ISBN', 'isbn')
        parse_field(key, 'Título', 'name')
        parse_field(key, 'Ent. princ.', 'author')
        parse_field(key, 'Assuntos', 'place')
        parse_field(key, 'Imprenta', 'year')
        parse_field(key, 'Edição', 'publisher')

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
    crawler_name = 'Sophia Crawler'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        driver.get('http://acervo.bn.br/sophia_web/index.html')
        print('%s: Finding iframe...' % crawler_name)
        find_iframe(driver)
        print('%s: Searching book by isbn...' % crawler_name)
        find_by_isbn(driver, term)
        print('%s: Taking the first book of the list' % crawler_name)
        take_book_on_list(driver)
        print('%s: Extracting book data...' % crawler_name)
        book_dict = extract_book_data_as_dict(driver)

        print('%s: Saving book...' % crawler_name)
        save_book(book_dict)

        print('%s: Book was saved!' % crawler_name)

        driver.close()

    except NoBookFoundError as e:
        print('%s: No book found!' % crawler_name)
        driver.close()

    except Exception as e:
        print(e)
        driver.close()
