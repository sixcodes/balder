import aiohttp
import asyncio
from utils import fetch
from schema import book_schema

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'
ISBN = '9788584390670'


async def fetch_book_found(http_session, url):
    data, status = await fetch(http_session, url)
    return book_schema(data)


async def search_for_isbn(http_session, url, isbn):
    data, status = await fetch(http_session, url.format(isbn))
    return data['items'][0] if data['totalItems'] > 0 else False


async def book_worker(aiohttp, url, isbn):
    async with aiohttp.ClientSession() as session:
        response = await search_for_isbn(session, url, isbn)
        if response:
            book_data = await fetch_book_found(session, response['selfLink'])
            return book_data
        else:
            return {'error': 'Livro não encontrado'}


async def main():
    book_data = await book_worker(aiohttp, BASE_URL, ISBN)
    if 'error' not in book_data:
        print(book_data)
    else:
        print(book_data['error'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
