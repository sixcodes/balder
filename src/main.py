import asyncio
from worker import book_worker
from file_reader import get_isbn_list_from_file

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'


async def main(loop):
    book_file = await get_isbn_list_from_file('src/isbn_list.txt')
    book_list = book_file.splitlines()

    tasks = asyncio.gather()

    for book in books:
        if 'error' not in book:
            print(book['title'])
        else:
            print(book['error'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_until_complete(loop.shutdown_asyncgens())
