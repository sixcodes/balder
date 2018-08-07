import aiohttp


def book_schema(plain_data):
    book = {}
    book['isbn'] = plain_data['volumeInfo']['industryIdentifiers'][1]['identifier']
    book['title'] = plain_data['volumeInfo']['title']
    book['authors'] = plain_data['volumeInfo']['authors']

    if 'description' in plain_data['volumeInfo']:
        book['description'] = plain_data['volumeInfo']['description']

    if 'published' in plain_data['volumeInfo']:
        book['published'] = plain_data['volumeInfo']['publishedDate']

    book['publisher'] = plain_data['volumeInfo']['publisher']
    book['country'] = plain_data['accessInfo']['country']

    return book


async def fetch(session, url):
    async with session.get(url) as response:
        status = response.status
        json = await response.json()
        return json, status


async def fetch_book_found(http_session, url):
    data, status = await fetch(http_session, url)
    return book_schema(data)


async def search_for_isbn(http_session, url, isbn):
    data, status = await fetch(http_session, url.format(isbn))
    return data['items'][0] if status == 200 and data['totalItems'] > 0 else False


async def fetch_book(url, isbn, aiohttp=aiohttp):
    async with aiohttp.ClientSession() as session:
        response = await search_for_isbn(session, url, isbn)
        if response:
            book_data = await fetch_book_found(session, response['selfLink'])
            return book_data
        else:
            return {'error': 'Livro {} não encontrado'.format(isbn)}
