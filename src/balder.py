from threading import Thread

from crawlers import crawl_dedalus, crawl_pucpr, crawl_sophia
from datasource import DBConnection


if __name__ == '__main__':
    DBConnection()

    isbn = '9788547302177'

    threads = [
        # Thread(target=crawl_dedalus, args=(isbn,)),
        Thread(target=crawl_sophia, args=(isbn,))
    ]

    for thread in threads:
        thread.start()
