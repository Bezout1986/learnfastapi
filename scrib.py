import time
import requests
import asyncio
import aiohttp

async def make_request(id, sleeptime):
    print(f"started {id} for {sleeptime} seconds")
    await asyncio.sleep(sleeptime)
    print(f"completed {id} after {sleeptime} seconds")
    return {"id": id , "data": f"this was coroutine {id}"}


async def main():
    task1=asyncio.create_task(make_request('a',4))
    task2=asyncio.create_task(make_request('b',8))
    task3=asyncio.create_task(make_request('c',1))

    res1=await task1
    res2=await task2
    res3=await task3

    results=await asyncio.gather(make_request('alpha',10),make_request('beta',2),make_request('gamma',6))

    #for resu in results:
        #print(f"received result {resu}")
asyncio.run(main())