from threading import Thread

from crawlers import crawl_sophia, crawl_dedalus
from datasource import DBConnection


if __name__ == '__main__':
    DBConnection()

    # isbn = '85-322-1022-8'
    isbn_sophia = '9788535911121'
    isbn_dedalus = '9788547302177'

    threads = [
        Thread(target=crawl_dedalus, args=(isbn_dedalus,)),
        Thread(target=crawl_sophia, args=(isbn_sophia,))
    ]

    for thread in threads:
        thread.start()
