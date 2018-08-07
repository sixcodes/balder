import asyncio
import json
from worker import book_worker
from file_reader import get_isbn_list_from_file

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'
CONCURRENT_DOWNLOADS = 2

queue = asyncio.Queue()

results = {
    'downloaded': [],
    'not_founds': [],
}


async def split_in_lines():
    book_file = await get_isbn_list_from_file('isbn_list.txt')
    return book_file.splitlines()


async def get_download_results(isbn, results, index, sem, queue=queue):
    print('start downloading {} number {}'.format(isbn, index))
    async with sem:
        book = await book_worker(BASE_URL, isbn)
        if 'error' not in book:
            results['downloaded'].append(book)
            queue.put({'downloaded': book})
            print(book['title'])
        else:
            results['not_founds'].append(isbn)
            queue.put({'not_found': isbn})
            print(book['error'])


async def write_results(queue=queue):
    while True:
        book = await queue.get()

        if 'downloaded' in book:
            write_book_found_result(book)


async def main():
    isbn_list = await split_in_lines()

    for index, isbn in enumerate(isbn_list):
        print(isbn)

    print('total of books {}'.format(len(isbn_list)))

    consumer = asyncio.ensure_future(write_results())

    sem = asyncio.Semaphore(CONCURRENT_DOWNLOADS)

    asyncio.gather(
        *(
            get_download_results(isbn, results, index, sem)
            for index, isbn in enumerate(isbn_list)
        )
    )

    await queue.join()
    consumer.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
