import asyncio
from typing import Sequence
import httpx
import time


async def download_url(url: str, session: httpx.AsyncClient):
    response = await session.get(url)
    return url, response.elapsed.microseconds / 1000


async def get_pings(urls: Sequence[str]):
    async with httpx.AsyncClient() as session:
        out = await asyncio.gather(
            *(asyncio.ensure_future(download_url(url, session)) for url in urls)
        )
    return {k: v for k, v in out}


if __name__ == "__main__":
    urls = [
        "https://google.com",
        "https://yahoo.com",
        "https://wikipedia.com",
        "https://www.pythonlikeyoumeanit.com/",
        "https://aslvrstn.com/",
        "https://www.smithfieldfoods.com/",
        "https://www.t-sg.jp/en/",
    ]
    start = time.time()
    res = asyncio.run(get_pings(urls))
    end = time.time()

    print(res)
    print(
        f"Got {len(urls)} pings in {end-start}s.\nSum of elapsed (s): {sum(res.values())/1000}\nMax elapsed (s): {max(res.values())/1000}"
    )
