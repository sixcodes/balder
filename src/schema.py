

def book_schema(plain_data):
    return {
        'isbn': plain_data['volumeInfo']['industryIdentifiers'][1]['identifier'],
        'title': plain_data['volumeInfo']['title'],
        'authors': plain_data['volumeInfo']['authors'],
        'description': plain_data['volumeInfo']['description'],
        'published': plain_data['volumeInfo']['publishedDate'],
        'publisher': plain_data['volumeInfo']['publisher'],
        'country': plain_data['accessInfo']['country']
    }
