
async def fetch(session, url):
    async with session.get(url) as response:
        status = response.status
        json = await response.json()
        return json, status
