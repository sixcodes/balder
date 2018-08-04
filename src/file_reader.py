import aiofiles


async def get_isbn_list_from_file(path, aiofiles=aiofiles):
    async with aiofiles.open(path, mode='r') as f:
        return await f.read()
