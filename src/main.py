import asyncio
from book_fetcher import fetch_book
from file_reader import get_isbn_list_from_file
from motor.motor_asyncio import AsyncIOMotorClient

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'
client = AsyncIOMotorClient('mongodb://localhost:27017')
mongo = client.balder

# Total de livros 208666


async def split_in_lines():
    book_file = await get_isbn_list_from_file('isbn_list-copy.txt')
    return book_file.splitlines()


async def get_download_results(isbn, index, sem, mongo=mongo):
    async with sem:
        print('start downloading {} number {}'.format(isbn, index))
        book = await fetch_book(BASE_URL, isbn)
        if 'error' not in book:
            try:
                await mongo.books.insert_one(book)
                print('========================>{}'.format(book['title']))
            except Exception as e:
                print('Book cannot be saved')
        else:
            print(book['error'])


async def main():
    isbn_list = await split_in_lines()

    for index, isbn in enumerate(isbn_list):
        print(isbn)

    print('total of books {}'.format(len(isbn_list)))

    sem = asyncio.Semaphore(20)

    asyncio.gather(
        *(
            get_download_results(isbn, index, sem)
            for index, isbn in enumerate(isbn_list)
        )
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.Task(main())
    loop.run_forever()
    print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
    loop.close()
