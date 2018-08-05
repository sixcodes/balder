import asyncio
import json
from worker import book_worker
from file_reader import get_isbn_list_from_file

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'

results = {
    'donwnloaded': [],
    'not_founds': [],
}


async def split_in_files():
    book_file = await get_isbn_list_from_file('isbn_list.txt')
    return book_file.splitlines()


async def get_download_results(isbn, results, index):
    print('start downloading {} number {}'.format(isbn, index))
    book = await book_worker(BASE_URL, isbn)
    if 'error' not in book:
        results['downloaded'].append(book)
        print(book['title'])
    else:
        results['not_founds'].append(isbn)
        print(book['error'])


async def main():
    isbn_list = await split_in_files()

    for isbn in isbn_list:
        print(isbn)

    print('total of books {}'.format(len(isbn_list)))

    return asyncio.gather(
        *[get_download_results(isbn, results, index) for index, isbn in enumerate(isbn_list)]
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    result_string = json.dumps(results)
    with open('results.json', 'x') as f:
        f.write(result_string)
