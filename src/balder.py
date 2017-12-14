from threading import Thread

from crawlers import crawl_sophia, crawl_dedalus, crawl_pucpr
from datasource import DBConnection


if __name__ == '__main__':
    DBConnection()

    isbn_pucpr = '978-85-359-1112-1'
    isbn_sophia = '9788535911121'
    isbn_dedalus = '9788547302177'

    threads = [
        Thread(target=crawl_dedalus, args=(isbn_dedalus,)),
        Thread(target=crawl_sophia, args=(isbn_sophia,)),
        Thread(target=crawl_pucpr, args=(isbn_pucpr,))
    ]

    for thread in threads:
        thread.start()
