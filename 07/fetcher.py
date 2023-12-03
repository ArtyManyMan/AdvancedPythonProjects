"""
fetcher
"""
import argparse
import asyncio
import aiohttp


COUNTER = 1


async def worker(que, pos):
    """function que_reader get element(str) from queue and call fetch
    with URL
    """
    global COUNTER

    while not que.empty():
        try:
            url = await que.get()
            result = await fetch(url)
            if isinstance(result, int):
                print(
                    f"Обработано {COUNTER} URLs. {url} status code is {result}. Worker number {pos}."
                )
                COUNTER += 1
            else:
                print(f"{result}. Worker number {pos}.")
        except asyncio.TimeoutError:
            print("Out of timeout")
        finally:
            que.task_done()


async def fetch(url):
    """function fetch get URL and makes a 'get' request.
    fetch is returning status of request or info about error
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as request:
                return request.status
    except aiohttp.ClientResponseError as err:
        return f"Response problem: {err}"
    except aiohttp.ClientError as err:
        return f"Connection problem: {err}"


async def main(workers_num):
    """function main is reading file (file should have one URL in line), adding
    URLs in async queue and starting async workers according to value quantity 'workers_num'
    """
    que = asyncio.Queue()

    tasks = [
        asyncio.create_task(worker(que, i))
        for i in range(workers_num)
    ]

    with open(file="url_lib.txt", mode="r", encoding="utf-8") as file:
        for _, line in enumerate(file):
            await que.put(line.strip())

    await que.join()

    for task in tasks:
        task.cancel()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for async fetching URLs from txt file"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=10, help="number of async workers"
    )
    args = parser.parse_args()

    asyncio.run(main(args.workers))
    print('Обработка окончена')
