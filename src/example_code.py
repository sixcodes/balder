# encoding: utf-8

from __future__ import print_function
import os
import asyncio
import ujson as json
import aiohttp
import aiofiles
import logging
import uvloop
from streamer import Streamer

import motor.motor_asyncio

# sync implementation too slow

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logging.getLogger('asyncio').setLevel(logging.DEBUG)

MOBICARE_USER = 'bemobi'
MOBICARE_PASS = 's3QEaD4EMSc6Xc2M'

conn = aiohttp.TCPConnector(limit=100)
sem = asyncio.Semaphore(50)
# queue = asyncio.Queue()

PRE_PAID = '/api/prePaid/msisdn/'
POST_PAID = '/api/postPaid/msisdn/'
HOST = 'https://oi-webservices-facade.mobicare.com.br/oi-wifi-webservices'
HEADERS = {'content-type': 'application/json',
           'X-FORCE-PREPAID-UPDATE': 'true', 'Accept': 'application/json'}

loop = asyncio.get_event_loop()

queue = Streamer(loop)

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://mongo:27017/axis?w=1&j=false&maxpoolsize=120', io_loop=loop)
db = client.get_default_database()


async def fetch(msisdn, session, sem=sem):

    print('msisdn', msisdn)
    user = b''
    with (await sem):
        # trying request as a pre paid msisdn
        async with session.get('{0}{1}{2}'.format(HOST, PRE_PAID, msisdn), auth=aiohttp.BasicAuth(MOBICARE_USER, MOBICARE_PASS), headers=HEADERS) as resp:
            user = await resp.read()
            if not user:
                async with session.get('{0}{1}{2}'.format(HOST, POST_PAID, msisdn), auth=aiohttp.BasicAuth(MOBICARE_USER, MOBICARE_PASS), headers=HEADERS) as resp:
                    user = await resp.read()
            return user

# TODO: Improve queue name to be flexible


async def read_file(filename, queue_name=None):
    async with aiofiles.open('files/'+filename, mode='r') as file:
        async for msisdn in file:
            msisdn = msisdn.strip()[2:]
            print('file_msisdn', msisdn)
            await queue.send_to_queue(queue_name, {'msisdn': msisdn})


async def pub(queue_name):
    """

    """
    async for item in db[queue_name].find({'processed': False}):
        item.pop('_id')
        await queue.send_to_queue(queue_name, item)
        print('publish msisdn', item['msisdn'])


async def sub(collection, queue_name):
    """
        Method to consume messages and save into DB
    """
    async with aiohttp.ClientSession() as session:
        while True:
            response = await queue.get_message(queue_name)
            events = response.get('Messages')
            if events:
                for event in events:
                    receipt = event.get('ReceiptHandle')
                    body = json.loads(event.get('Body'))
                    print(body)
                    msisdn = body.get('msisdn')
                    print('subscriber: ', msisdn)

                    user = await db.users.find_one({'$or': [{'subscriber': msisdn}, {'msisdn': msisdn}]})
                    if not user:
                        user = await fetch(msisdn, session)
                        print('response user: ', user)
                    if user:
                        if isinstance(user, dict):
                            user.pop('_id')
                        else:
                            user = json.loads(user.decode())
                        subscriber = user.get('subscriber') or user.get('msisdn')
                        await db[collection].update({'subscriber': subscriber}, user, upsert=True)
                    await queue.delete_message(queue_name, receipt)


async def run():
    """
        Running app
    """
    for filename in os.listdir('./files'):
        asyncio.ensure_future(read_file(filename, 'oilivre-oicloud-process'))
    for _ in range(500):
        asyncio.ensure_future(sub('oicloud', 'oilivre-oicloud-process'))

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    asyncio.Task(run())
    loop.run_forever()
    print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
    loop.close()
