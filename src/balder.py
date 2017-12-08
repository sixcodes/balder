import sys
import os
from threading import Thread

from crawlers.dedalus import crawl_dedalus
from datasource import DBConnection


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('balder.py'))
    DBConnection()

    t_dedalus = Thread(target=crawl_dedalus, args=('9788547302177',))
    t_dedalus.start()
